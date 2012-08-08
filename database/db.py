import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker

import logging

from base import *
from obj import *

class Db():
    
    base = Base
    FORMAT = '%(levelname)s - %(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('database')
    engine = create_engine('sqlite:///cache.db', echo=True)
    Session = sessionmaker(bind=engine)

    def __init__(self):
        self.base.metadata.create_all(self.engine)
        self.__session = self.Session()

    def commit(self):
        try:
            self.__session.commit()
        except exc.IntegrityError:
            self.logger.warning('Feed already in base')
            self.__session.rollback()

    def add_feed(self, url):
        f = feed.Feed(url)
        f.parse_info()
        print f.info
        self.__session.add(f)

    def get_feeds(self):
        return self.__session.query(feed.Feed).all()

    def update_news(self):
        for f in self.get_feeds():
            self.update_news_one_feed(f)

    def update_news_one_feed(self,feed):
        #Create new session,because maybe we will be multi thread
        s=self.Session()
        feed.load_info()
        print feed.data
        feed.load_news(s)
        s.commit()