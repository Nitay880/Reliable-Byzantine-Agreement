import threading
import random
from Constants import N, F, MESSAGE_LENGTH

# todo: split messages if _str_ > message length, barrier has to be N-F
barrier = threading.Barrier(N-F)
leader=0
c=0
def ideal_functionality():
    global c
    global leader
    barrier.wait()
    if (c%(N-F))==0:
        leader=random.randint(0,N-1)
    c+=1
    return leader
def recieve_message(client_socket):
    try:
        message_header = client_socket.recv(MESSAGE_LENGTH)
        if not len(message_header):
            return False
        message_header = message_header.decode("utf-8").strip("*")
        return message_header
    except:
        return False


def send_message(client_socket, message):
    try:
        mes_str = message.__str__()

        mes_str += '*' * (MESSAGE_LENGTH - len(mes_str))
        client_socket.send(bytes(mes_str, encoding='utf8'))
    except:
        return False
