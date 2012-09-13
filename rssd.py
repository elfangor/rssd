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
        feeds=list()
        for f in self.db.get_feeds():
            feeds.append(f.get_info())
        return feeds
    
    def get_news(self,param):            
        news=list()
        if("feed" in param):
            for n in self.db.get_news(param['feed']):
                yield n.get_info()
        else:
            pass
