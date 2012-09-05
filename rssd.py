from twisted.internet import reactor

from database.db import Db
from network.factory import RssdFactory


class Rssd():
    def __init__(self):
        self.db = Db()
        reactor.listenTCP(8123, RssdFactory(self))
        reactor.run()

    def update(self):
        self.db.update_news()
