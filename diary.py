import os
import json

# Module Imports
import mariadb
import sys

# Get Cursor
cur = conn.cursor()

class Diary(object):

    def __init__(self):
        self.connect()

    def connect(self):
        # Connect to MariaDB Platform
        try:
            self.conn = mariadb.connect(
                user="dizzy",
                password="aPutzUNh2mSAwk84",
                host="192.168.1.42",
                port=3306,
                database="dizzy"

            )
            self.cur = conn.cursor()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
    
    def update(self):
        for name, path in self.tables.items():
            
            if not os.path.isfile(path):
                self.data[name] = {}
            elif name not in self.data:
                self.data[name] = json.loads(open(path).read())
            else:
                self.data[name].clear()
                self.data[name].update(json.loads(open(path).read()))
        return self.data
        
    def save(self):
        for name, path in self.tables.items():
            with open(path, 'w') as f:
                f.write(json.dumps(self.data[name], indent=4))
        return self.data
        
def publisher(config):
    if config["DB_Type"] == 'FlatJson':
        return FlatJson(config)
    else:
        raise Exception("DB_Type unhandled.")