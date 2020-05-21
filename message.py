"""


          ____                                                                                     ,--,
        ,'  , `.                                                                                 ,--.'|
     ,-+-,.' _ |                                                                                 |  | :
  ,-+-. ;   , ||          .--.--.    .--.--.                ,----._,.                            :  : '                 .--.--.    .--.--.
 ,--.'|'   |  || ,---.   /  /    '  /  /    '    ,--.--.   /   /  ' /   ,---.             ,---.  |  ' |     ,--.--.    /  /    '  /  /    '
|   |  ,', |  |,/     \ |  :  /`./ |  :  /`./   /       \ |   :     |  /     \           /     \ '  | |    /       \  |  :  /`./ |  :  /`./
|   | /  | |--'/    /  ||  :  ;_   |  :  ;_    .--.  .-. ||   | .\  . /    /  |         /    / ' |  | :   .--.  .-. | |  :  ;_   |  :  ;_
|   : |  | ,  .    ' / | \  \    `. \  \    `.  \__\/: . ..   ; ';  |.    ' / |        .    ' /  '  : |__  \__\/: . .  \  \    `. \  \    `.
|   : |  |/   '   ;   /|  `----.   \ `----.   \ ," .--.; |'   .   . |'   ;   /|        '   ; :__ |  | '.'| ," .--.; |   `----.   \ `----.   \
|   | |`-'    '   |  / | /  /`--'  //  /`--'  //  /  ,.  | `---`-'| |'   |  / |        '   | '.'|;  :    ;/  /  ,.  |  /  /`--'  //  /`--'  /
|   ;/        |   :    |'--'.     /'--'.     /;  :   .'   \.'__/\_: ||   :    |        |   :    :|  ,   /;  :   .'   \'--'.     /'--'.     /
'---'          \   \  /   `--'---'   `--'---' |  ,     .-./|   :    : \   \  /          \   \  /  ---`-' |  ,     .-./  `--'---'   `--'---'
                `----'                         `--`---'     \   \  /   `----'            `----'           `--`---'
                                                             `--`-'
The following represent a message
############
::source -  message sender
::target -  message reciever
::value -   message content
::view -    in what view the message is sent
::world -   in what world the message lives (0..N-1)
############
"""


class Message:
    def __init__(self, source, target, type, value, view, world):
        self._value = value
        self._view = view
        self._world = world
        self._source = source
        self._target = target
        self._type = type

    def get_view(self):
        return self._view

    def get_value(self):
        return self._value

    def __str__(self):
        return str(self._source) + "|" + str(self._target) + "|" + str(self._type) + "|" + str(self._value) + "|" + str(
            self._view) + "|" + str(self._world)

    def decode(self, message):
        source, target, value, view, world = message.split("|")
        return message(source, target, value, view, world)
