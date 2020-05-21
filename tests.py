from Constants import host, port, N,F
import threading
from server import server
from mediator import mediator
from Constants import LONG_DELAY,NO_DELAY
import signal
def regular_case():
    servers = []
    servers_threads = []
    # initiate and run mediator
    mediator_server = mediator(host, port)
    med_th = threading.Thread(target=mediator_server.work)
    med_th.start()
    # initiate and run servers
    for i in range(N):
        servers.append(server(host, port, i))
        servers_threads.append(threading.Thread(target=servers[-1].start_work))
    for s in servers_threads:
        s.start()

def bad_leader_is_elected_once():
    servers = []
    servers_threads = []
    # initiate and run mediator
    mediator_server = mediator(host, port)
    med_th = threading.Thread(target=mediator_server.work)
    med_th.start()
    # initiate and run servers
    for i in range(N):
        servers.append(server(host, port, i))
        servers_threads.append(threading.Thread(target=servers[-1].start_work))
    for s in servers_threads:
        s.start()
    for s in servers_threads:
        s.join()
def long_delay():
    servers = []
    servers_threads = []
    # initiate and run mediator
    mediator_server = mediator(host, port,long_delay=LONG_DELAY)
    med_th = threading.Thread(target=mediator_server.work)
    med_th.start()
    # initiate and run servers
    for i in range(N):
        servers.append(server(host, port, i))
        servers_threads.append(threading.Thread(target=servers[-1].start_work))
    for s in servers_threads:
        s.start()
def no_delay():
    servers = []
    servers_threads = []
    # initiate and run mediator
    mediator_server = mediator(host, port,long_delay=NO_DELAY)
    med_th = threading.Thread(target=mediator_server.work)
    med_th.start()
    # initiate and run servers
    for i in range(N):
        servers.append(server(host, port, i))
        servers_threads.append(threading.Thread(target=servers[-1].start_work))
    for s in servers_threads:
        s.start()
