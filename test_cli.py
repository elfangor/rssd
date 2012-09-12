import json

from twisted.internet import reactor, protocol
import time
import os.path
from twisted.protocols.basic import LineReceiver

class EchoClient(LineReceiver):

    def connectionMade(self):
        self.sendLine("blabla")
        self.authen()
#        self.sendLine(json.dumps({"cmd":"get_feeds"}))
        self.sendLine(json.dumps({"cmd":"add_feed","param":{"feed":'http://archlinux.fr/feed'}}))
        self.sendLine(json.dumps({"cmd":"update"}))
#        self.sendLine(json.dumps({"cmd":"update"}))


#        self.sendLine("hej")
#        self.sendLine("wa")

    def connectionLost(self, reason):
        print "connection lost"

    def lineReceived(self, line):
        print line

    def authen(self):
        self.sendLine(json.dumps({"cmd":"login","param":{"login":"test","pass":"ok"}}))

class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()


# this connects the protocol to a server runing on port 8000
def main():
    f = EchoFactory()
    reactor.connectTCP("localhost", 8123, f)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
