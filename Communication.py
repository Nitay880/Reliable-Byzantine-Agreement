import threading
import multiprocessing
import random
from Constants import N, F, MAX_MESSAGE_LENGTH
import signal

# todo: split messages if _str_ > message length, barrier has to be N-F
barrier = multiprocessing.Barrier(N - F)
leader = 0
c = 0


def block_sig(func):
    def call(*args, **kwargs):
        signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGALRM])
        result = func(*args, **kwargs)
        signal.pthread_sigmask(signal.SIG_UNBLOCK, [signal.SIGALRM])

        return result

    return call


def ideal_functionality():
    """The following function is responsible for leader election scheme. It contains a multiprocessing.barrier
    which waits for N-F processors and then picks a leader and terminates
    Returns:
        leader -- id of the current leader
    """
    print("*****in ideal functionality*******")
    global c
    global leader
    barrier.wait()
    if (c % (N - F)) == 0:
        leader = random.randint(0, N - 1)
    c += 1
    return leader


def recieve_message(client_socket):
    try:
        message_header = client_socket.recv(MAX_MESSAGE_LENGTH)
        if not len(message_header):
            return False
        message_header = message_header.decode("utf-8").strip("*")
        return message_header
    except Exception as e:
        #print(e)
        return False


def send_message(client_socket, message):
    try:
        mes_str = message.__str__()
        mes_str += '*' * (MAX_MESSAGE_LENGTH - len(mes_str))
        client_socket.send(bytes(mes_str, encoding='utf8'))
    except Exception  as e:
        print(e)
        return False
