import logging
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from database.base import *

class New(Base):
    __tablename__ = 'news'

    id_news = Column(Integer,primary_key=True)
    gid = Column(String,unique=True)
    author = Column(String)
    title = Column(String)
    link = Column(String)
    is_read = Column(Boolean)
    content = Column(String)
    insert_date = Column(DateTime)
    id_feeds = Column(Integer, ForeignKey('feeds.id_feeds'))

    feed = relationship("Feed",backref=backref('news', order_by=id_news))

    FORMAT = '%(levelname)s - %(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('new')

    def __init__(self,id_feed,data):
        self.id_feeds = id_feed
        self.insert_date = datetime.today()
        if 'author' in data:
            self.author = data['author']
        else:
            self.logger.warning('No author setting to none')
            self.author = None
        if "title" in data:
            self.title = data['title']
        else:
            self.logger.warning('No title setting to none')
            self.title = None
        if "id" in data:
            self.gid = data['id']
        #TODO: adding a error handling: raise error when no id
        if "content" in data:
            self.content = data['content'][0]['value']
        else:
            self.logger.warning('No content trying with summary')
            if "summary_detail" in data:
                self.content = data['summary_detail']['value']
            else:
                self.logger.warning('No content seting to None')
                self.content = None
            
        if "link" in data:
            self.link = data['links'][0]['href']
        else:
            self.logger.warning('No link setting to none')
            self.link = None

    def get_info(self,json=True):
        if json:
            return {"id_feed":self.id_feeds,"id_new":self.id_news,"link": self.link,"title":self.title,"insert_date":str(self.insert_date),"is_read":self.is_read,"content":self.content,"author":self.author,"gid":self.gid}
        else:
            return {"id_feed":self.id_feeds,"id_new":self.id_news,"link": self.link,"title":self.title,"insert_date":self.insert_date,"is_read":self.is_read,"content":self.content,"author":self.author,"gid":self.gid}
