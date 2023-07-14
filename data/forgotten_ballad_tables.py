import sqlite3
conn = sqlite3.connect("roll_tables.db")
cur = conn.cursor()

cur.execute("DROP TABLE rolltables")
cur.execute("CREATE TABLE rolltables(game, name, dice, roll, result)")

cur.execute("""
    INSERT INTO rolltables VALUES
        ('Forgotten Ballad', 'Relic Type', '1d6', 1, 'Weapon:>Forgotten Ballad>Weapon >> Property:>Forgotten Ballad>Relic Property'),
        ('Forgotten Ballad', 'Relic Type', '1d6', 2, 'Weapon:>Forgotten Ballad>Weapon >> Property:>Forgotten Ballad>Relic Property'),
        ('Forgotten Ballad', 'Relic Type', '1d6', 3, 'Armor:>Forgotten Ballad>Armor >> Property:>Forgotten Ballad>Relic Property'),
        ('Forgotten Ballad', 'Relic Type', '1d6', 4, 'Armor:>Forgotten Ballad>Armor >> Property:>Forgotten Ballad>Relic Property'),
        ('Forgotten Ballad', 'Relic Type', '1d6', 5, 'Instrument:>Forgotten Ballad>Instrument >> Property:>Forgotten Ballad>Relic Property'),
        ('Forgotten Ballad', 'Relic Type', '1d6', 6, 'Utility:>Forgotten Ballad>Utility >> Property:>Forgotten Ballad>Relic Property')
""")

cur.execute("""
    INSERT INTO rolltables VALUES
        ('Forgotten Ballad', 'Weapon', '1d3||1d6', 11, 'Sword'),
        ('Forgotten Ballad', 'Weapon', '1d3||1d6', 12, 'Quiver'),
        ('Forgotten Ballad', 'Weapon', '1d3||1d6', 13, 'Scythe'),
        ('Forgotten Ballad', 'Weapon', '1d3||1d6', 14, 'Bow'),
        ('Forgotten Ballad', 'Weapon', '1d3||1d6', 15, 'Staff'),
        ('Forgotten Ballad', 'Weapon', '1d3||1d6', 16, 'Spear'),
        ('Forgotten Ballad', 'Weapon', '1d3||1d6', 21, 'Hammer'),
        ('Forgotten Ballad', 'Weapon', '1d3||1d6', 22, 'Axe'),
        ('Forgotten Ballad', 'Weapon', '1d3||1d6', 23, 'Halberd'),
        ('Forgotten Ballad', 'Weapon', '1d3||1d6', 24, 'Boomerang'),
        ('Forgotten Ballad', 'Weapon', '1d3||1d6', 25, 'Club'),
        ('Forgotten Ballad', 'Weapon', '1d3||1d6', 26, 'Explosive'),
        ('Forgotten Ballad', 'Weapon', '1d3||1d6', 31, 'Trident'),
        ('Forgotten Ballad', 'Weapon', '1d3||1d6', 32, 'Wand'),
        ('Forgotten Ballad', 'Weapon', '1d3||1d6', 33, 'Gauntlet'),
        ('Forgotten Ballad', 'Weapon', '1d3||1d6', 34, 'Scimitar'),
        ('Forgotten Ballad', 'Weapon', '1d3||1d6', 35, 'Gauntlet'),
        ('Forgotten Ballad', 'Weapon', '1d3||1d6', 36, 'Whip')
""")

cur.execute("""
    INSERT INTO rolltables VALUES
        ('Forgotten Ballad', 'Armor', '1d6', 1, 'Shield'),
        ('Forgotten Ballad', 'Armor', '1d6', 2, 'Armor/Tunic'),
        ('Forgotten Ballad', 'Armor', '1d6', 3, 'Mask'),
        ('Forgotten Ballad', 'Armor', '1d6', 4, 'Boots'),
        ('Forgotten Ballad', 'Armor', '1d6', 5, 'Gloves'),
        ('Forgotten Ballad', 'Armor', '1d6', 6, 'Bracelet')
""")
            
cur.execute("""
    INSERT INTO rolltables VALUES
        ('Forgotten Ballad', 'Instrument', '1d2||1d6', 11, 'Ocarina'),
        ('Forgotten Ballad', 'Instrument', '1d2||1d6', 12, 'Harp'),
        ('Forgotten Ballad', 'Instrument', '1d2||1d6', 13, 'Flute'),
        ('Forgotten Ballad', 'Instrument', '1d2||1d6', 14, 'Cornet'),
        ('Forgotten Ballad', 'Instrument', '1d2||1d6', 15, 'Mandolin'),
        ('Forgotten Ballad', 'Instrument', '1d2||1d6', 16, 'Banjo'),
        ('Forgotten Ballad', 'Instrument', '1d2||1d6', 21, 'Drum'),
        ('Forgotten Ballad', 'Instrument', '1d2||1d6', 22, 'Bell'),
        ('Forgotten Ballad', 'Instrument', '1d2||1d6', 23, 'Organ'),
        ('Forgotten Ballad', 'Instrument', '1d2||1d6', 24, 'Violin'),
        ('Forgotten Ballad', 'Instrument', '1d2||1d6', 25, 'Triangle'),
        ('Forgotten Ballad', 'Instrument', '1d2||1d6', 26, 'Guitar')
""")
cur.execute("""
    INSERT INTO rolltables VALUES
        ('Forgotten Ballad', 'Utility', '1d3||1d6', 11, 'Hook'),
        ('Forgotten Ballad', 'Utility', '1d3||1d6', 12, 'Telescope'),
        ('Forgotten Ballad', 'Utility', '1d3||1d6', 13, 'Mirror'),
        ('Forgotten Ballad', 'Utility', '1d3||1d6', 14, 'Book'),
        ('Forgotten Ballad', 'Utility', '1d3||1d6', 15, 'Lantern'),
        ('Forgotten Ballad', 'Utility', '1d3||1d6', 16, 'Remedy'),
        ('Forgotten Ballad', 'Utility', '1d3||1d6', 21, 'Candle'),
        ('Forgotten Ballad', 'Utility', '1d3||1d6', 22, 'Flippers'),
        ('Forgotten Ballad', 'Utility', '1d3||1d6', 23, 'Camera'),
        ('Forgotten Ballad', 'Utility', '1d3||1d6', 24, 'Shovel'),
        ('Forgotten Ballad', 'Utility', '1d3||1d6', 25, 'Backpack'),
        ('Forgotten Ballad', 'Utility', '1d3||1d6', 26, 'Rope'),
        ('Forgotten Ballad', 'Utility', '1d3||1d6', 31, 'Bag'),
        ('Forgotten Ballad', 'Utility', '1d3||1d6', 32, 'Bottle'),
        ('Forgotten Ballad', 'Utility', '1d3||1d6', 33, 'Seeds'),
        ('Forgotten Ballad', 'Utility', '1d3||1d6', 34, 'Stick'),
        ('Forgotten Ballad', 'Utility', '1d3||1d6', 35, 'Magnifying glass'),
        ('Forgotten Ballad', 'Utility', '1d3||1d6', 36, 'Egg')
""")
cur.execute("""
    INSERT INTO rolltables VALUES
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 11, 'Giant'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 12, 'Fairy'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 13, 'Electricity'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 14, 'Poison'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 15, 'Distance'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 16, 'Wisdom'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 21, 'Explosion'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 22, 'Leadership'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 23, 'Ceremony'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 24, 'Moon'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 25, 'Light'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 26, 'Fortune'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 31, 'Fast'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 32, 'Aroma'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 33, 'Dance'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 34, 'Insect'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 35, 'Darkness'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 36, 'Magnetic'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 41, 'Talk'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 42, 'Plant'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 43, 'Size'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 44, 'Fire'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 45, 'Rock'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 46, 'Monster'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 51, 'Stone'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 52, 'Time'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 53, 'Ice'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 54, 'Power'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 55, 'Song'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 56, 'Friend'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 61, 'Disguise'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 62, 'Water'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 63, 'Sand'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 64, 'Truth'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 65, 'Courage'),
            ('Forgotten Ballad', 'Relic Property', '1d6||1d6', 66, 'Cure')
            """)

conn.commit()
# print(cur.execute("SELECT * FROM rolltables").fetchall())