import sqlite3
conn = sqlite3.connect("../data/twit_tables.db")
cur = conn.cursor()

def setup():
    
    cur.execute("DROP TABLE opted")
    cur.execute("CREATE TABLE opted(guild, user)")
    cur.execute("CREATE UNIQUE INDEX opted_idx1 on opted(guild, user)")

    conn.commit()
    
def check():
    print(cur.execute("SELECT * FROM opted").fetchall())
    
if __name__ == '__main__':
  import fire
  fire.Fire()