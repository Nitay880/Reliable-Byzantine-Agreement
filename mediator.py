from random import randint
import select
import socket
from message import Message
from Communication import recieve_message, send_message
import Constants
from Constants import host,port,DELAY,F,N
import time
import signal

"""
                                                                                                 
          ____                                                                                   
        ,'  , `.                                                    ___                          
     ,-+-,.' _ |                  ,---,   ,--,                    ,--.'|_                        
  ,-+-. ;   , ||                ,---.'| ,--.'|                    |  | :,'     ,---.     __  ,-. 
 ,--.'|'   |  ;|                |   | : |  |,                     :  : ' :    '   ,'\  ,' ,'/ /| 
|   |  ,', |  ':    ,---.       |   | | `--'_        ,--.--.    .;__,'  /    /   /   | '  | |' | 
|   | /  | |  ||   /     \    ,--.__| | ,' ,'|      /       \   |  |   |    .   ; ,. : |  |   ,' 
'   | :  | :  |,  /    /  |  /   ,'   | '  | |     .--.  .-. |  :__,'| :    '   | |: : '  :  /   
;   . |  ; |--'  .    ' / | .   '  /  | |  | :      \__\/: . .    '  : |__  '   | .; : |  | '    
|   : |  | ,     '   ;   /| '   ; |:  | '  : |__    ," .--.; |    |  | '.'| |   :    | ;  : |    
|   : '  |/      '   |  / | |   | '/  ' |  | '.'|  /  /  ,.  |    ;  :    ;  \   \  /  |  , ;    
;   | |`-'       |   :    | |   :    :| ;  :    ; ;  :   .'   \   |  ,   /    `----'    ---'     
|   ;/            \   \  /   \   \  /   |  ,   /  |  ,     .-./    ---`-'                        
'---'              `----'     `----'     ---`-'    `--`---'                                      
                                                                                                 """
Animation= "|/-\\"


class mediator:
    def __init__(self, host, port, delay=0):
        """
        :param host: host ip
        :param port: host port
        :param long_delay: 0 no delay, 1 long delay, 2 moderate delay
        """
        self._quit=False
        self._leader = 0
        self._view = 0
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((host, port))
        self._host = host
        self._port = port
        self._socket.setblocking(False)
        self._socket.listen()
        self._client_sockets = {}
        self._sockets = [self._socket]
        self._registered = 0
        self._pending = []
        self._num_of_connected = 0
        self._delta=delay
        self._send_omission = []
        self._recieve_omission = []
        for i in range(F):
            #at most F 
            ommited = str(randint(0,N-1))
            self._send_omission.append(ommited)
            self._recieve_omission.append(ommited)
        signal.signal(signal.SIGALRM, self.out_pending_messages)
        signal.alarm(1)

    def work(self):
        while True:
            if self._quit:
                self.close_connection()
            read_sockets, _, exeption_sockets = select.select(self._sockets, [], self._sockets)
            for notified_socket in read_sockets:
                if notified_socket == self._socket:
                    # it's the first message that is sent from this socket
                    client_socket, client_address = self._socket.accept()
                    message = recieve_message(client_socket)
                    print(message)
                    if message is False:
                        continue
                    self._sockets.append(client_socket)
                    this_user_id = message.split("|")[0]
                    self._num_of_connected+=1
                    self._client_sockets[this_user_id]=client_socket
                    mes = Message('med',this_user_id , "SYN-ACK", '', 0, message.split("|")[-1])
                    send_message(client_socket, mes)
                else:
                    message = recieve_message(notified_socket)
                    waiting_time = randint(0, self._delta)
                    self._pending.append((message, time.time(), waiting_time))
                    if message is False:
                        self._sockets.remove(notified_socket)
                        continue
            for notified_socket in exeption_sockets:
                self._sockets.remove(notified_socket)
    def out_pending_messages(self, signum, frame):
        if self._num_of_connected < Constants.N:
            print("mediator is waiting for N servers to initiation  pending:"+str(len(self._pending)),end="\r")
            print(len(self._pending))
            signal.alarm(1)
            return
        N = len(self._pending)
        i = 0
        #print(N)
        to_print="0"*(3-len(str(len(self._pending))))
        print("mediator is Delivering "+to_print+str(len(self._pending)), end="\r")
        while i < N:
            if (time.time() - self._pending[i][Constants.STARTING_TIME]) >= self._pending[i][Constants.WAITING_TIME]:
                message = self._pending.pop(i)[0]
                N -= 1
                i -= 1
                self.deliver_message(message)
            i += 1
        signal.alarm(1)
    
    def close_connection(self):
        self._socket.close()
        exit(1)
    def deliver_message(self, message):
        # print(message)
        if message==False:
            return
        message_source, message_target, message_type, message_content, message_view, message_world = message.split("|")
        # case this message isn't to the mediator
        if message_target != 'med':
            if message_target in self._client_sockets.keys() and message_target not in self._recieve_omission and message_source not in self._send_omission:
                target_socket = self._client_sockets[message_target]
                # here the omission fauilure comes into play
                # todo: as this is an asynchrnous, delay messages from time to time via clock - signals and uniform random delay DONE
                send_message(target_socket,
                             Message(message_source, message_target, message_type, message_content, message_view,
                                     message_world))
    def set_quit(self):
        self._quit=True
if __name__=="__main__":
    med=mediator(host,port,DELAY)
    med.work()
