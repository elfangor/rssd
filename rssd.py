from database.db import Db

class Rssd():
    def __init__(self):
        self.db = Db()

    def update(self):
        self.db.update_news()
