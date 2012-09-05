from twisted.internet.protocol import Factory

from protocol import Protocol


class RssdFactory(Factory):

    def __init__(self,rssd):
        self.rssd = rssd

    def buildProtocol(self, addr):
        return Protocol(self.rssd)


