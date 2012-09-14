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
            yield {"cmd":"get_feeds","results":f.get_info()}
    
    def get_news_id(self,param=None):            
        if param and "feed" in param:
            for n in self.db.get_news(param['unread'],param['feed']):
                yield {"cmd":"get_news","results":n.id_news}
        else:
            for n in self.db.get_news():
                yield {"cmd":"get_news","results":n.id_news}

    def get_news(self,param=None):            
        if param and "feed" in param:
            for n in self.db.get_news(param['unread'],param['feed']):
                yield {"cmd":"get_news","results":n.get_info()}
        else:
            for n in self.db.get_news():
                yield {"cmd":"get_news","results":n.get_info()}

    def set_read(self,param):
        self.db.get_new(param['new']).is_read=True
        self.db.commit()
