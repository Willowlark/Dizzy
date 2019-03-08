import os
import json

class FlatJson(object):

    def __init__(self, config):
        self.db_name = config["DB_Name"]
        self.db = config["DB"]
        self.tables = config["Tables"]

        self.data = {}
        self.connect()

    def connect(self):
        os.chdir(self.db)
        self.update()
        return self.data
    
    def update(self):
        for name, path in self.tables.items():
            if name not in self.data:
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