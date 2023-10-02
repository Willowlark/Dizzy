import sqlite3
conn = sqlite3.connect("../data/roll_tables.db")
cur = conn.cursor()

def setup():

    # cur.execute("DROP TABLE rolltables")
    cur.execute("CREATE TABLE rolltables(game, name, dice, roll, 'result')")

    conn.commit()

def check():
    print(cur.execute("SELECT * FROM rolltables").fetchall())
    
if __name__ == '__main__':
  import fire
  fire.Fire()