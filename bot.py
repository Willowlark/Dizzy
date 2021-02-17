import mariadb
import pandas as pd
from numpy import nan

import commands
from datetime import datetime


class Engine(object):

    def __init__(self):
        self.diary = Diary()
        self.build_snowflake()
        self.collection = CommandCollection(self.raw_cmds, self.diary)
        
    def build_snowflake(self):
        # Tables to build snowflak
        servers = self.diary.pd_execute("SELECT * FROM SERVERS")
        commands = self.diary.pd_execute("SELECT * FROM COMMANDS")
        server_commands = self.diary.pd_execute("SELECT * FROM JOIN_SERVERS_COMMANDS")
        prefixes = self.diary.pd_execute("SELECT * FROM SERVER_PREFIXES").drop('ID',axis=1)
        whitelists = self.diary.pd_execute("SELECT * FROM COMMAND_WHITELISTS")
        
        # Join Servers and Commands
        snowflake = server_commands.merge(servers, on='SERVER_ID')
        self.snowflake = snowflake.merge(commands, on='COMMAND_ID')
        self.snowflake = self.snowflake.merge(whitelists, left_on='AUTHOR_WHITELIST', right_on='ID', how='outer').drop('ID_y',axis=1)
        
        
        # The universal prefixes are applied by server_id = 1. As these will only apply to server 
        # 1 (All Servers) if we merge as is, we duplicate the server_id=1 rows for each of the other
        # servers defined. This way every server has a copy of the universal prefixes, and when we 
        # merge the snowflake with prefixes, commands that are unique to a server get the server_id=1
        # prefixes as well
        x = prefixes[prefixes.SERVER_ID==1].copy().drop('SERVER_ID',axis=1)
        y = servers[servers.SERVER_ID!=1].SERVER_ID.to_frame() 
        x['FLAG'] = 1
        y['FLAG'] = 1
        ap = x.merge(y,on='FLAG').drop('FLAG',axis=1)
        self.prefixes = prefixes.append(ap)
        
        # Filter out the commands with a unique prefix. By design, if CMD_TRIGGER is filled in, 
        # That's the only trigger that should activate the command. Therefore we can't merge any
        # row with CMD_TRIGGER != NULL or the default prefixes above will be applied to it.
        x = self.snowflake[~self.snowflake['CMD_TRIGGER'].isnull()]
        y = self.snowflake[self.snowflake['CMD_TRIGGER'].isnull()]
        raw_cmds = y.merge(self.prefixes,on='SERVER_ID')
        self.raw_cmds = x.append(raw_cmds).reset_index()
        
        
        # Servers + Logs, specific for logging. 
        logs = self.diary.pd_execute("SELECT * FROM SERVER_LOGS").drop('ID',axis=1)
        self.logs = servers.merge(logs, on='SERVER_ID')

    async def on_message(self, message):
    
        await self.collection.execute(message)
        self.log(message)
        
    def log(self, message):
        pass
    
class Diary(object):

    def __init__(self):
        self.data_tables = []
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
            # self.cur = self.conn.cursor()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
    
    def pd_execute(self, query):
        return pd.read_sql(query, self.conn)
    
    def get_data_table(self, table_name):
        query = f"select * from {table_name}"
        data = self.pd_execute(query)
        self.data_tables.append([query, data])
        return data
    
    def update(self):
        for name, path in self.data_tables.items():
            
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
        
class CommandCollection(object):
    
    def __init__(self, raw_cmds, diary):
        self.commands = []
        self.generate(raw_cmds, diary)
    
    def generate(self, raw_cmds, diary):
        
        raw_cmds = raw_cmds.replace({nan: None})
        dicts = raw_cmds.to_dict(orient='index')
        
        for key in dicts:
            cmd_spec = dicts[key]
            
            cmd_class = commands.REFERENCE[cmd_spec['PYTHON_CLASS']]
            cmd_trigger = cmd_spec['CMD_TRIGGER'] if cmd_spec['CMD_TRIGGER'] else cmd_spec['PREFIX']
            if cmd_spec['OPTIONS_FROM_DB']:
                cmd_options = diary.get_data_table(cmd_spec['OPTIONS'])
            else:
                cmd_options = cmd_spec['OPTIONS']
            cmd_pattern = cmd_spec['PATTERN']
            cmd_info = cmd_spec['HELP']
            cmd_author = cmd_spec['AUTHOR']
            
            self.commands.append(cmd_class(triggers=cmd_trigger, options=cmd_options, pattern=cmd_pattern, info=cmd_info, author=cmd_author))
    
    async def execute(self, message):
        for command in self.commands:
            if await command.execute(message):
                break
    
if __name__ == '__main__':
    self = Engine()