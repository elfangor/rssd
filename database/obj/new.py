from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from database.base import *

class New(Base):
    __tablename__ = 'news'

    id_news = Column(Integer,primary_key=True)
    author = Column(String)
    title = Column(String)
    link = Column(String)
    is_read = Column(Boolean)
    content = Column(String)
    insert_date = Column(DateTime)
    id_feeds = Column(Integer, ForeignKey('feeds.id_feeds'))

    feed = relationship("Feed",backref=backref('news', order_by=id_news))

    def __init__(self,id_feed,data):
        self.id_feeds = id_feed
        self.insert_date = datetime.today()
        self.author = data['author']
        self.title = data['title']
        self.content = data['content'][0]['value']
        self.link = data['links'][0]['href']


