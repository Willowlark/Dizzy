import mariadb
import pandas as pd
from numpy import nan
from datetime import datetime

import commands
import logger
from auth import MARIADB_PASS

class Engine(object):

    def __init__(self):
        self.diary = Diary()
        self.build_snowflake()
        self.collection = CommandCollection(self.raw_cmds, self.diary)
        self.logmanager = LogManager(self.raw_logs, self.diary)
        
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
        self.raw_logs = servers.merge(logs, on='SERVER_ID')

    async def on_message(self, message):
    
        await self.collection.execute(message)
        self.logmanager.log(message)
        
class Diary(object):
    
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        # Connect to MariaDB Platform
        try:
            self.conn = mariadb.connect(
                user="dizzy",
                password=MARIADB_PASS,
                host="192.168.1.42",
                port=3306,
                database="dizzy",
                autocommit=True
            )
            
            # self.cur = self.conn.cursor()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
    
        return self.conn
    
    def pd_execute(self, query):
        return pd.read_sql(query, self.conn)

    def get_data_table(self, table_name):
        query = f"select * from {table_name}"
        data = self.pd_execute(query)
        data['MODIFIED_BIT'] = False
        return data
        
    def save(self, table_name, newdata):
        
        if not table_name:
            # This command triggers a rebuiuld but has nothing to save
            return None
            
        cur = self.conn.cursor()
        pks = list(self.pd_execute(f"SHOW KEYS FROM {table_name} WHERE Key_name = 'PRIMARY'").Column_name)
        
        if 'RM' in newdata.columns:
            indexes = []
            for index, row in newdata[newdata.RM == True].iterrows():
                where_str = []
                for pk in pks:
                    where_str.append(f"{pk} = {row[pk]}")
                where_str = ', '.join(where_str)
                delete_query = f"DELETE FROM {table_name} WHERE {where_str};"
                print(delete_query)
                cur.execute(delete_query)
                indexes.append(index)
            newdata = newdata.drop(indexes)
            newdata = newdata.drop('RM',axis=1)
        
        update_set = newdata[newdata.MODIFIED_BIT == True].drop('MODIFIED_BIT', axis=1)
        
        update_columns = set(update_set.columns) - set(pks)
        for index, row in update_set.iterrows():
            
            update_str = []
            for up in update_columns:
                up_v = f"'{self.conn.escape_string(row[up])}'" if type(row[up]) is str else row[up]
                update_str.append(f"{up} = {up_v}")
            update_str = ', '.join(update_str)
            
            insert_str = []
            for insert in list(update_set.columns):
                insert_v = f"'{self.conn.escape_string(row[insert])}'" if type(row[insert]) is str else row[insert]
                insert_str.append(f"{insert_v}")
            insert_str = ', '.join(insert_str)
            update_query = f"INSERT INTO {table_name} VALUES ({insert_str}) ON DUPLICATE KEY UPDATE {update_str};"
            print(update_query)
            cur.execute(update_query)
        
class CommandCollection(object):
    
    def __init__(self, raw_cmds, diary):
        self.commands = []
        self.diary = diary
        self.raw_cmds = raw_cmds
        self.generate(raw_cmds)
    
    def generate(self, raw_cmds):
        
        raw_cmds = raw_cmds.replace({nan: None})
        dicts = raw_cmds.to_dict(orient='index')
        
        for key in dicts:
            cmd_spec = dicts[key]
            # TODO: Move this parse into the Command Init, IE pass in cmd_spec & options
            
            cmd_class = commands.REFERENCE[cmd_spec['PYTHON_CLASS']]
            cmd_trigger = cmd_spec['CMD_TRIGGER'] if cmd_spec['CMD_TRIGGER'] else cmd_spec['PREFIX']
            if cmd_spec['OPTIONS_FROM_DB']:
                cmd_options = self.diary.get_data_table(cmd_spec['OPTIONS'])
                cmd_options_source = cmd_spec['OPTIONS']
            else:
                cmd_options = cmd_spec['OPTIONS']
                cmd_options_source = None
            cmd_pattern = cmd_spec['PATTERN']
            cmd_info = cmd_spec['HELP']
            cmd_author = cmd_spec['AUTHOR']
            cmd_updates = cmd_spec['UPDATE_ON_CALL']
            
            self.commands.append(cmd_class(triggers=cmd_trigger, options=cmd_options, options_source=cmd_options_source, pattern=cmd_pattern, info=cmd_info, author=cmd_author, update_me=cmd_updates))
    
    def rebuild(self):
        self.commands = []
        self.generate(self.raw_cmds)
        print("Local Cache Rebuilt")
    
    async def execute(self, message):
        for command in self.commands:
            res = await command.execute(message)
            if res:
                if command.update_me:
                    self.diary.save(command.options_source, command.options)
                    self.rebuild()
                break

class LogManager(object):
    
    def __init__(self, raw_logs, diary):
        self.logs = {}
        self.diary = diary
        self.raw_logs = raw_logs
        self.generate(raw_logs)
        
    def generate(self, raw_logs):
        dicts = raw_logs.to_dict(orient='index')
        
        for key in dicts:
            log_spec = dicts[key]
            log_class = logger.REFERENCE[log_spec['LOG_TYPE']]
            log_uid = log_spec['UID']
            log_target = log_spec['LOG_TARGET']
            
            x = log_class(log_target)
            if log_uid in self.logs:
                self.logs[log_uid].append(x)
            else:
                self.logs[log_uid] = [x]
        
    def log(self, message):
        
        if message.guild.id in self.logs:
            for log in self.logs[message.guild.id]:
                log.log(message)
        
if __name__ == '__main__':
    self = Engine()