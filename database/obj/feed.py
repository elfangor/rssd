import feedparser
from time import mktime
from datetime import datetime
import logging

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from new import New

from database.base import *

class Feed(Base):
    __tablename__ = 'feeds'

    id_feeds = Column(Integer,primary_key=True)
    url = Column(String, unique=True)
    title = Column(String)
    link = Column(String)
    subtitle = Column(String)
    updated = Column(DateTime)
    insert_date = Column(DateTime)

    FORMAT = '%(levelname)s - %(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('feed')

    def __init__(self,url=None):
        if not url.startswith('http'):
            self.logger.warning('URL not starting with http adding it')
            url = 'http://' + url
        self.url = url
        self.insert_date = datetime.today()
        if url:
            self.load_info()

    def load_info(self):
        self.data = feedparser.parse(self.url)
        self.info=self.data.feed

    def load_news(self,session):
        print "STARTING LOAD NEWS"
        n=[]
        for item in self.data['entries']:
           n.append(New(self.id_feeds,item))
        session.add_all(n)

    def parse_info(self):
        self.link = self.info['link']
        self.subtitle = self.info['subtitle']
        self.title = self.info['title']
        self.updated = datetime.fromtimestamp(mktime(self.info['updated_parsed']))

    def get_info(self,json=True):
        if json:
            return {"id_feed":self.id_feeds,"link": self.link,"subtitle":self.subtitle,"title":self.title,"update":str(self.updated)}
        else:
            return {"id_feed":self.id_feeds,"link": self.link,"subtitle":self.subtitle,"title":self.title,"update":self.updated}
