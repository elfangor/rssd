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

    def add_feed(self,param):
        self.db.add_feed(param['feed'])

    def get_feeds(self):
        for f in self.db.get_feeds():
            yield f.get_info()
    
    def get_news(self,param):            
        if("feed" in param):
            for n in self.db.get_news(param['feed']):
                yield n.get_info()
        else:
            pass
