from cloudant import client
from scribe import Scribe
import asyncio
import os
import json

class Diary(object):

    def __init__(self, username, password):
        self.user = username
        self.password = password
        self.connection = client.Cloudant(username, password, account=username, connect=True)
        self.db_name = ""
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
        try:
            return True if self.db is not None and self.db.exists() else False
        except:
            self.connection = client.Cloudant(self.user, self.password, account=self.user, connect=True)
            self.db = self.connection[self.db_name]
            return True if self.db is not None and self.db.exists() else False
            

    def select_db(self, db):
        try:
            self.db = self.connection[db]
            self.scribe.scribe("selected Database '{}'".format(db))
            self.db_name = db
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

    def save_document(self, key, value):
        value.save()


class Offline_Diary(object):

    def __init__(self, username, password):
        self.user = username
        self.password = password
        self.db_name = ""
        self.db = '.' # a folder
        self.scribe = Scribe('error')

    def db_required(function):
        def wrapper(instance, *args, **kwargs):
            if instance.active_db():
                return function(instance, *args, **kwargs)
            else:
                instance.scribe.scribe("Function {} requires an selected database.".format(function), 'error')
        return wrapper

    def active_db(self):
        return True if os.path.isdir(self.db) else False

    def select_db(self, db):
        if os.path.isdir(db): 
            os.chdir(db)
            self.db_name = db

    @db_required
    def load_document(self, key):
        document = json.loads(open(key+'.json').read())
        return document
    
    def create_document(self, json):
        return False

    def save_document(self, key, value):
        with open(key+'.json', 'w') as f:
            f.write(json.dumps(value))

if __name__ == '__main__':

    d = Offline_Diary('user', 'password')
    d.select_db('.')
    doc = d.load_document('sets')
    print(doc)
    # doc['memes'] = 100
    # doc.save()
    # d.create_document({"_id" : "Willowlark"})