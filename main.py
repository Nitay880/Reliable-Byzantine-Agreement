from Constants import host, port, N,F
import threading
from server import server
from mediator import mediator
import signal
import sys
import platform
from subprocess import Popen
import random 
print(host, port)

port=port+random.randint(0,9)
if __name__ == "__main__":
    
    servers = []
    servers_threads = []
    # initiate and run mediator
    mediator_server = mediator(host, port)
    med_th = threading.Thread(target=mediator_server.work)
    med_th.start()
    # initiate and run servers
    for i in range(N):
        servers.append(server(host, port,i))
        servers_threads.append(threading.Thread(target=servers[-1].start_work))
    for s in servers_threads:
        s.start()

    while True:
        states = []
        for server in servers:
            states.append(server.get_stage())
        if states.count("DECIDED") >= N - F:
            print("decision has made!")
            for server in servers:
                server.close_connection()
            mediator_server.close_connection()
            exit(1)