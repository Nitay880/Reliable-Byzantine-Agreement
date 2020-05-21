from message import Message
from Communication import send_message
import socket


class client:
    def __init__(self, mediator_host, mediator_port):
        self._client_messages = []
        self._mediator_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._mediator_socket.connect((mediator_host, mediator_port))
        self._mediator_socket.setblocking(False)

    def work(self):
        while True:
            value = input('Please type your value, client:')
            send_message(self._mediator_socket, Message('client', 'med', 'client-message', value, 0, 0))
