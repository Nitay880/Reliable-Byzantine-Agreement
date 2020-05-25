"""
Message class  - 

The following represents a message
############
public fields:
::source -  message sender
::target -  message reciever
::value -   message content
::view -    in what view the message is sent
::world -   in what world the message lives (0..N-1)
############
"""


class Message:
    def __init__(self, source, target, type, value, view, world,lock="*"):
        """[summary]

        Arguments:
            source {[who send this message]} -- [id of the sender (processor number)]
            target {[destination/goal entity]} -- [id of the destination (i.e proc no.)]
            type {[message's role]} -- [echo/vc-blame etc.]
            value {[int/string]} -- [the value of the sender]
            view {[the view in which the message sended]} -- [each message is sended in some view]
            world {[the world in which the message sended]} -- [each message is sended in some world]
        """
        self._value = value
        self._view = view
        self._world = world
        self._source = source
        self._target = target
        self._type = type
        self._lock=lock

    def get_view(self):
        """The following function returns the message view

        Returns:
            [String/int] -- [The view which the message sended in]
        """
        return self._view

    def get_value(self):
        """The following function returns the value that is stored in that message 
        Returns:
            [String] -- [The value to echo/send/decide on]
        """
        return self._value

    def __str__(self):
        return str(self._source) + "|" + str(self._target) + "|" + str(self._type) + "|" + str(self._value) + "|" + str(
            self._view) + "|" + str(self._world)+"|"+str(self._lock)
