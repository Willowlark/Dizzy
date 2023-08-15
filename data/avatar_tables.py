import sqlite3
conn = sqlite3.connect("roll_tables.db")
cur = conn.cursor()

# cur.execute("DROP TABLE rolltables")
# cur.execute("CREATE TABLE rolltables(game, name, dice, roll, 'result')")

# Dice notation same as used by Dice Cog
# Prefix>game>table >> ...

cur.execute("""
    INSERT INTO rolltables VALUES
        ('Avatar TTRPG', 'Name', '1d4', 1, 'Name:>Avatar TTRPG>Fire Nation Names'),
        ('Avatar TTRPG', 'Name', '1d4', 2, 'Name:>Avatar TTRPG>Air Nomad Names'),
        ('Avatar TTRPG', 'Name', '1d4', 3, 'Name:>Avatar TTRPG>Earth Kingdom Names'),
        ('Avatar TTRPG', 'Name', '1d4', 4, 'Name:>Avatar TTRPG>Water Tribe Names')
""")

cur.execute("""
    INSERT INTO rolltables VALUES
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 1, 'Aditi'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 2, 'Akash'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 3, 'Anil'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 4, 'Baljin'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 5, 'Batsal'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 6, 'Chaha'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 7, 'Chime'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 8, 'Chimini'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 9, 'Devna'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 10, 'Diki'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 11, 'Dronma'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 12, 'Ehani'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 13, 'Gawa'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 14, 'Gedun'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 15, 'Jetsun'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 16, 'Mukta'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 17, 'Samlo'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 18, 'Toofan'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 19, 'Yeshe'),
        ('Avatar TTRPG', 'Air Nomad Names', '1d20', 20, 'Zaya')
""")

cur.execute("""
    INSERT INTO rolltables VALUES
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 1, 'Binh'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 2, 'Bowen'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 3, 'Caihong'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 4, 'Chia-Hao'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 5, 'Dae'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 6, 'Diu'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 7, 'Hanna'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 8, 'Heng'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 9, 'Kim'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 10, 'Kyung'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 11, 'Minh'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 12, 'Nuan'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 13, 'Qiang'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 14, 'Quiyue'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 15, 'Shufen'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 16, 'Thi'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 17, 'Woong'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 18, 'Xiaobo'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 19, 'Ya-Ting'),
        ('Avatar TTRPG', 'Earth Kingdom Names', '1d20', 20, 'Zixin')
""")

cur.execute("""
    INSERT INTO rolltables VALUES
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 1, 'Achak'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 2, 'Aklaq'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 3, 'Aputi'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 4, 'Atka'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 5, 'Hanta'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 6, 'Kallik'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 7, 'Kanti'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 8, 'Kitchi'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 9, 'Makwa'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 10, 'Meeka'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 11, 'Miki'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 12, 'Niimi'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 13, 'Noodin'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 14, 'Siqniq'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 15, 'Tapisa'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 16, 'Thaki'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 17, 'Ukiuk'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 18, 'Waaseyaa'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 19, 'Yuka'),
        ('Avatar TTRPG', 'Water Tribe Names', '1d20', 20, 'Ziibi')
""")

cur.execute("""
    INSERT INTO rolltables VALUES
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 1, 'Asayo'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 2, 'Ayami'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 3, 'Bashira'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 4, 'Davaa'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 5, 'Erdene'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 6, 'Ganzaya'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 7, 'Hanako'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 8, 'Jaw'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 9, 'Long'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 10, 'Kayo'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 11, 'Keisuke'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 12, 'Kenshin'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 13, 'Manami'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 14, 'Mayu'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 15, 'Qacha'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 16, 'Qudan'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 17, 'Satsuki'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 18, 'Saya'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 19, 'Tuguslar'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 20, 'Yuka'),
        ('Avatar TTRPG', 'Fire Nation Names', '1d21', 21, 'Zolzaya')
""")

conn.commit()
# print(cur.execute("SELECT * FROM rolltables").fetchall())