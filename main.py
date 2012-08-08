from database.db import Db

if __name__ == '__main__':
    db = Db()
    db.add_feed('http://archlinux.fr/feed')
    db.commit()
    db.update_news()
#    db.add_feed('http://feeds.feedburner.com/bashfr')
