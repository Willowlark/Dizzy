import csv
import glob
from os.path import basename, dirname, exists
import sqlite3
conn = sqlite3.connect("../../data/rollable.db")
cur = conn.cursor()

def setup(csv_file='table_index.csv'):

    cur.execute("DROP TABLE rollable")
    cur.execute("CREATE TABLE rollable(id INTEGER PRIMARY KEY, database, table_name, die_code, prefix, postfix)")
    table = "rollable"

    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(f"""
                        INSERT INTO {table} 
                        (database, table_name, die_code, prefix, postfix)
                        VALUES 
                        (:database,:table_name,:die_code,:prefix,:postfix)""", row)
    conn.commit()
    print(cur.execute(f"SELECT * FROM {table}").fetchall())

    conn.commit()

def lst(table='rollable'):
    conn = sqlite3.connect(f"../../data/{table}.db")
    cur = conn.cursor()
    r = cur.execute("SELECT tbl_name FROM sqlite_master where type='table'")
    
    for y in r.fetchall():
        print(y)

def build(db):
    tables = cur.execute(f'SELECT table_name FROM rollable WHERE database="{db}"').fetchall()
    print("Bulk Adding:", tables)
    for t in tables:
        add(t[0])

def add(csv_file):
    
    if not exists(csv_file):
        csv_file = _find_file(csv_file)
    
    table = basename(csv_file)[:-4].lower().replace(' ', "_")
    schema = dirname(csv_file).split('/')[-1]#.lower().replace(' ', "_")
    
    conn = sqlite3.connect(f"../../data/{schema}.db")
    cur = conn.cursor()
    try:
        cur.execute(f"DROP TABLE {table}")
    except sqlite3.OperationalError:
        pass
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table}(roll integer, return, cnt_schema, cnt_table)")
    conn.commit()
    
    _load_csv(schema, table, csv_file)
    print(f"Added {csv_file}")

def _load_csv(schema, table, csv_file):
    
    conn = sqlite3.connect(f"../../data/{schema}.db")
    cur = conn.cursor()
    
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(f"INSERT INTO {table} VALUES (:roll, :return, :cnt_schema, :cnt_table)", row)
    conn.commit()
    
def _find_file(filename):
    ret = glob.glob(f'**/*{filename}*')
    if len(ret) == 1: return ret[0]
    else: raise Exception(f"Not a specific enough filename. Matched: \n{ret}")

if __name__ == '__main__':
  import fire
  fire.Fire()