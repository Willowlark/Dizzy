from cloudant import client
from scribe import Scribe
import asyncio

class Diary(object):

    def __init__(self, username, password):
        self.connection = client.Cloudant(username, password, account=username, connect=True)
        self.curr_db = ""
        self.db = None
        self.scribe = Scribe('error')

    def db_required(function):
        def wrapper(instance, *args, **kwargs):
            if instance.active_db():
                return function(instance, *args, **kwargs)
            else:
                instance.scribe.scribe("Function {} requires an selected database.".format(function), 'error')
        return wrapper

    def active_db(self):
        return True if self.db is not None and self.db.exists() else False

    def select_db(self, db):
        try:
            self.db = self.connection[db]
            self.scribe.scribe("selected Database '{}'".format(db))
        except KeyError:
            self.scribe.scribe("No Database '{}'; load failed. No database selected.".format(db), 'error')
            self.db = None

    @db_required
    def load_document(self, key):
        from time import sleep
        document = self.db[key]
        return document
    
    def create_document(self, json):
        document = self.db.create_document(json)
        return document


if __name__ == '__main__':
    username = "0b7824b2-ff6a-43c8-b37e-770568551b7e-bluemix"
    password = "0b7998d6d61162eba46ef2c369c22b4beab3237596454454017196b65389f1a4"

    d = Diary(username, password)
    d.select_db('dizzy')
    doc = d.load_document('stats')
    # doc['memes'] = 100
    # doc.save()
    # d.create_document({"_id" : "Willowlark"})