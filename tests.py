from Constants import host, port, N, F, DELAY
import threading
from server import server
from mediator import mediator
import multiprocessing
from multiprocessing import Lock
import random
from Communication import ideal_functionality, block_sig
import signal

num_of_times = 0
leader = 0
c = 0
mutex = Lock()
port = port + random.randint(0, 9)
print(host, port)
mediator_server = mediator(host, port, DELAY)
barrier = multiprocessing.Barrier(N - F)


def bad_leader_is_elected_i(k=1):
    global num_of_times
    global mediator_server
    num_of_times = k
    servers = []
    servers_threads = []
    # initiate and run mediator
    med_th = threading.Thread(target=mediator_server.work)
    med_th.start()
    # initiate and run servers

    for i in range(N):
        servers.append(server(host, port, i,ideal_functionality))
        servers_threads.append(threading.Thread(target=servers[-1].start_work))
    for s in servers_threads:
        s.start()
    while True:
        states = []
        for s in servers:
            states.append(s.get_stage())
        if states.count("DECIDED") >= N - F:
            print("*****decision has made!****")
            for s in servers:
                s.set_quit()
            mediator_server.set_quit()
            exit(1)


def ideal_functionality():
    print("*****in ideal functionality*******")
    global c
    global leader
    global mutex
    global mediator_server
    global num_of_times
    global barrier
    barrier.wait()
    mutex.acquire()

    if (c % (N - F) == 0):
        leader = mediator_server.get_omissioned() if (c // (N - F)) < num_of_times else mediator_server.get_active()
    c += 1
    mutex.release()
    return int(leader)


def all_nice_and_no_ommited_elected():
    bad_leader_is_elected_i(0)


def bad_leader_is_elected():
    bad_leader_is_elected_i(2)


if __name__ == "__main__":
    # all_nice_and_no_ommited_elected()
    bad_leader_is_elected()
