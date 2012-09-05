from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class Protocol(LineReceiver):
    def __init__(self,deamon):
        self.auth= False
        self.deamon = deamon

    def lineReceived(self, line):
        if line == "update":
            print "update"
            self.deamon.update()
