import sqlite3
conn = sqlite3.connect("../data/role_tables.db")
cur = conn.cursor()

def setup():
    
    cur.execute("DROP TABLE assignable")
    cur.execute("CREATE TABLE assignable(guild, role)")
    cur.execute("CREATE UNIQUE INDEX assignable_idx1 on assignable(guild, role)")
    
    cur.execute("DROP TABLE managers")
    cur.execute("CREATE TABLE managers(guild, user)")
    cur.execute("CREATE UNIQUE INDEX managers_idx1 on managers(guild, user)")

    conn.commit()
    
def check():
    print(cur.execute("SELECT * FROM assignable").fetchall())
    print(cur.execute("SELECT * FROM managers").fetchall())
    
if __name__ == '__main__':
  import fire
  fire.Fire()