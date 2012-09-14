import json

from twisted.internet import reactor, protocol
import time
import os.path
from twisted.protocols.basic import LineReceiver

class EchoClient(LineReceiver):
    MAX_LENGTH=99999999

    def connectionMade(self):
        self.authen()
        self.sendLine(json.dumps({"cmd":"add_feed","param":{"feed":"http://feeds.feedburner.com/bashfr-quotes?format=xml"}}))
        self.sendLine(json.dumps({"cmd":"update"}))
        self.sendLine(json.dumps({"cmd":"get_news","param":{"feed":1,"unread":True}}))
#        self.sendLine(json.dumps({"cmd":"get_feeds"}))

    def connectionLost(self, reason):
        print "connection lost"

    def lineReceived(self, line):
        print "transaction incomming"
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
