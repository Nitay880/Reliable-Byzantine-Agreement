import socket
import sys
import errno
from message import Message
from Constants import N,F,port,host
from Communication import recieve_message, send_message,ideal_functionality

"""                                                              
Server Code (A single processor/Thread)   
"""


class server:
    def __init__(self,mediator_host= host,mediator_port=port,id="*"):
        """
        :param mediator_host:  host name of the mediator (socket details)
        :param mediator_port:  port of mediator socket   (socket details)
        :param id: server's id (0,...,N-1)               (protocol detail)
        """
        # each server starts with an id
        self._quit=False
        self._id=id
        self._stage = "COMMUNICATION_INITIALIZATION"
        # value::the value i locked on world i
        # lock::the view that i decided value in world i
        # view::current view in world i
        self._views = [0 * i for i in range(N)]
        self._locks = [0 * i for i in range(N)]
        self._values = [0 * i for i in range(N)]
        # if i heard from the leader in world i, heard[i]=True
        self._heard = [False] * N
        self._values[self._id] = self._id
        self._ack_messages_in_my_world = 0
        # VC DataStructures
        self._vc_value_gather = {}
        self._vc_blame_gather = 0
        self._done_counter = 0
        self._mediator_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._mediator_socket.connect((mediator_host, mediator_port))
        except:
            self.logit("Mediator Server is Off")
            return
        self._mediator_socket.setblocking(False)
        self._current_leader = 0
        # send first message to the mediator
        mes = Message(self._id, "med", "SYN", '', self._views[self._id], self._id)
        send_message(self._mediator_socket, mes)
    def rm_log(self):
        with open(str(self._id)+".txt", 'w') as f:
            pass
    def close_connection(self):
        self._mediator_socket.close()
        self.rm_log()
        exit(1)
    def logit(self,output):
        with open(str(self._id)+".txt", 'a') as f:
            f.write(output+'\n')
    def reset_my_world(self):
    
        self._done_counter = 0
        self._views[self._id] += 1
        self._locks[self._id] += 1
        self._stage = "SEND"
        self._ack_messages_in_my_world = 0
        self._vc_blame_gather = 0
        self._vc_value_gather = {}
        self._heard = [False] * N

    def start_work(self):
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:
            if self._quit:
                self.close_connection()
            try:
                # retrieve message
                self.state_driven()
                mes = recieve_message(self._mediator_socket)
                mes and self.message_driven(mes)
                mes and self.logit(mes)


            except IOError as e:
                # This is normal on non blocking connections - when there are no incoming data error is going to be raised
                # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
                # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
                # If we got different error code - something happened
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    self.logit('Reading error: {}'.format(str(e)))
                    sys.exit()
            except Exception as e:
                # Any other exception - something happened, exit
                self.logit('Reading error: '.format(str(e)))
                sys.exit()

    def state_driven(self):
        if self._stage == "SEND":
            self.logit("SENDING")
            for i in range(N):
                send_message(self._mediator_socket,
                             Message(self._id, i, "value", self._values[self._id], self._views[self._id], self._id))
            self._stage = "ACK"

        if self._ack_messages_in_my_world >= N - F and self._stage == "ACK":
            self.logit('world ' + str(self._id) + ' done')
            for i in range(N):
                send_message(self._mediator_socket, Message(self._id, i, "done", '', self._views[self._id], self._id))
            self._stage = "DONE"

        if self._done_counter >= N - F and self._stage == "DONE":
            # Leader election
            self._current_leader = ideal_functionality()
            self.logit("LE DONE LEADER IS " + str(self._current_leader))
            self._stage = "VC"  # done is sent once...
            type = "vc-value-gather" if self._heard[self._current_leader] else "vc-blame"
            for i in range(N):
                send_message(self._mediator_socket,
                             Message(self._id, i, type, self._values[self._current_leader],
                                     self._locks[self._current_leader], self._current_leader))
    def set_quit(self):
        self._quit=True
    def message_driven(self, mes):
        # retrieve mes
        message_source, message_target, message_type, message_content, message_view, message_world = mes.split("|")
        message_world = int(message_world)
        message_view = int(message_view)
        if message_type=="SYN-ACK" and message_source=="med":
            if self._id=="*":
                self._id=int(message_target)
                self._values[self._id] = self._id
            self._stage = "SEND"
            self.logit("Server "+str(self._id)+"is connected to the Med!")
        if self._stage == "VC":
            self.vc_handler(message_type, message_view, message_world, message_content)
        # echo message
        if message_type.startswith("echo"):
            if message_view >= self._locks[message_world]:
                self._values[message_world] = message_content
                self._locks[message_world] = message_view
            self._heard[message_world] = True
        # ack message
        elif message_type.startswith("ack"):
            self.ack_handler(message_content, message_view, message_world)
        elif message_type.startswith("done"):
            self._done_counter += 1
        elif message_type.startswith('value'):
            # recieved this message from the primary of some world i
            if message_view >= self._locks[message_world]:
                # lock this value
                self._values[message_world] = message_content
                self._locks[message_world] = message_view
            for i in range(N):
                # echo to all
                send_message(self._mediator_socket,
                             Message(self._id, i, 'echo ', message_content, message_view, message_world))
            # ack the primary
            send_message(self._mediator_socket,
                         Message(self._id, message_world, 'ack ', message_content, message_view,
                                 message_world))

    def vc_handler(self, message_type, message_view, message_world, message_content):
        if message_type.startswith("vc-value-gather") and message_world == self._current_leader:
            if (message_view, message_content) in self._vc_value_gather.keys():
                self._vc_value_gather[(message_view, message_content)] += 1
            else:
                self._vc_value_gather[(message_view, message_content)] = 1
        elif message_type.startswith("vc-blame") and message_world == self._current_leader:
            self._vc_blame_gather += 1

        if self._vc_blame_gather >= N - F:
            # VIEW CHANGE,RESTART MY WORLD
            self.reset_my_world()

        else:
            for key, value in self._vc_value_gather.items():
                if value >= N - F:
                    self.decide(key)

    def decide(self, key):
        self._values[self._current_leader] = key[1]
        self._locks[self._current_leader] = key[0]
        self.logit("*" + str(self._id) + ' decided ' + str(self._values[self._current_leader]) + ' on view ' + str(
            key[0]) + "*")
        self._stage = "DECIDED"
        self.close_connection()

    def get_stage(self):
        return self._stage
    def ack_handler(self, message_content, message_view, message_world):
        if message_world == self._id and message_view == self._views[self._id] and message_content == self._values[
            self._id]:
            self._ack_messages_in_my_world += 1
if __name__=="__main__":
    s=server(host,port)
    s.start_work()