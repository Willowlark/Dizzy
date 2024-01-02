import sqlite3
conn = sqlite3.connect("../data/trainer_rewards.db")
cur = conn.cursor()

def setup():
    
    cur.execute("DROP TABLE IF EXISTS class")
    cur.execute("CREATE TABLE class(name, cash integer)")
    
    cur.execute("DROP TABLE IF EXISTS rank")
    cur.execute("CREATE TABLE rank(name, multiplier integer)")

    conn.commit()
    
def check():
    print(cur.execute("SELECT * FROM class").fetchall())
    print(cur.execute("SELECT * FROM rank").fetchall())
    
def load():
   
    cur.execute("INSERT INTO class VALUES"
                "('Actor', 40),"
                "('Admin', 75),"
                "('Aether Branch Chief', 120),"
                "('Aether Foundation', 240),"
                "('Aether Foundation Employee', 48),"
                "('Aether President', 240),"
                "('Aroma Lady', 35),"
                "('Artist', 54),"
                "('Backers', 48),"
                "('Backpacker', 38),"
                "('Baker', 40),"
                "('Battle Girl', 28),"
                "('Beauty', 67),"
                "('Ranchers', 112),"
                "('Bellhop', 40),"
                "('Biker', 24),"
                "('Bird Keeper', 34),"
                "('Black Belt', 32),"
                "('Boarder', 52),"
                "('Boss', 140),"
                "('Boss Trainer', 200),"
                "('Brains & Brawn', 84),"
                "('Bug Catcher', 14),"
                "('Bug Maniac', 44),"
                "('Burglar', 72),"
                "('Butler', 80),"
                "('Cabbie', 120),"
                "('Cafe Master Tier 1', 80),"
                "('Cafe Master Tier 2', 120),"
                "('Cafe Master Tier 3', 160),"
                "('Cameraman', 41),"
                "('Captain', 120),"
                "('Champion', 187),"
                "('Channeler', 34),"
                "('Chef', 42),"
                "('Office Worker', 63),"
                "('Clown', 24),"
                "('Coach Trainer', 100),"
                "('Collector', 46),"
                "('Cook', 80),"
                "('Ace Trainer', 59),"
                "('Cowgirl', 16),"
                "('Roughneck', 27),"
                "('Cyclist', 32),"
                "('Dancer', 45),"
                "('Delinquent', 32),"
                "('Rail Staff', 80),"
                "('Doctor', 90),"
                "('Dojo Master Tier 1', 140),"
                "('Dojo Master Tier 2', 200),"
                "('Dojo Master Tier 3', 400),"
                "('Dojo Matron', 160),"
                "('Dragon Tamer', 47),"
                "('Driver', 64),"
                "('Eevee User', 88),"
                "('Elder', 120),"
                "('Elite Four', 131),"
                "('Engineer', 53),"
                "('Espeon User', 40),"
                "('Executive', 76),"
                "('Expert', 60),"
                "('Fairy Tale Girl', 24),"
                "('Firebreather', 40),"
                "('Firefighter', 40),"
                "('Fisher', 40),"
                "('Flareon User', 40),"
                "('Free Diver', 40),"
                "('Furisode Girl', 72),"
                "('Gambler', 96),"
                "('GAME FREAK', 125),"
                "('Gardener', 64),"
                "('Gentleman', 155),"
                "('Glaceon User', 200),"
                "('Golfer', 60),"
                "('Grunt', 40),"
                "('Guitarist', 30),"
                "('Gym Challenger', 140),"
                "('Gym Trainer', 96),"
                "('Harlequin', 32),"
                "('Hex Maniac', 27),"
                "('Hiker', 43),"
                "('Hooligans', 64),"
                "('Hoopster', 100),"
                "('Idol', 72),"
                "('Infielder', 100),"
                "('Island Kahuna', 160),"
                "('Janitor', 40),"
                "('Jogger', 32),"
                "('Jolteon User', 200),"
                "('Picnicker', 19),"
                "('Camper', 19),"
                "('Juggler', 37),"
                "('Kantonian Gym', 32),"
                "('Kimono Girl', 96),"
                "('Kindler', 32),"
                "('Lady', 160),"
                "('Lass', 26),"
                "('Gym Leader', 127),"
                "('Gym Leader (Rematch)', 240),"
                "('Leafeon User', 24),"
                "('League Staff', 100),"
                "('Linebacker', 100),"
                "('Lorekeeper', 100),"
                "('Lumiose Gang Member', 80),"
                "('Macro Cosmos Employee', 100),"
                "('Macro Cosmos Vice President', 140),"
                "('Macro Cosmos President', 200),"
                "('Maid', 40),"
                "('Master Dojo Student', 80),"
                "('Medium', 44),"
                "('Model', 120),"
                "('Monsieur', 200),"
                "('Motorcyclist', 32),"
                "('Musician', 48),"
                "('Mysterious Sisters', 54),"
                "('Mystery Man', 110),"
                "('Ninja Boy', 12),"
                "('Nurse', 40),"
                "('Nursery Aide', 40),"
                "('Police Officer', 56),"
                "('Old Couple', 120),"
                "('Owner', 90),"
                "('Painter', 16),"
                "('Parasol Lady', 34),"
                "('Pilot', 60),"
                "('Poke Fan Family', 160),"
                "('Poke Kid', 28),"
                "('Poke Fan', 72),"
                "('Poke Maniac', 50),"
                "('Pokemon Breeder', 53),"
                "('Pokemon Professor', 190),"
                "('Pokemon Ranger', 58),"
                "('Rival', 87),"
                "('Postman', 96),"
                "('Preschooler', 11),"
                "('Principal', 96),"
                "('Proprietor', 80),"
                "('Psychic', 32),"
                "('Punk Couple', 96),"
                "('Punk Girl', 33),"
                "('Punk Guy', 32),"
                "('Rancher', 40),"
                "('Rangers', 160),"
                "('Reporter', 43),"
                "('Rich Boy', 160),"
                "('Rising Star', 54),"
                "('Rocker', 26),"
                "('Roller Skater', 32),"
                "('Ruin Maniac', 43),"
                "('Sage', 40),"
                "('Sailor', 40),"
                "('Schoolboy', 47),"
                "('School Kid', 25),"
                "('Schoolgirl', 52),"
                "('Scientist', 57),"
                "('Scuba Diver', 40),"
                "('Secret Base Expert', 60),"
                "('Secret Base Trainer', 20),"
                "('Sightseer', 60),"
                "('Skier', 52),"
                "('Sky Trainer', 100),"
                "('Smasher', 100),"
                "('Socialite', 200),"
                "('Sootopolitan', 120),"
                "('Street Thug', 32),"
                "('Striker', 100),"
                "('Subway Boss', 100),"
                "('Successor', 160),"
                "('Super Nerd', 29),"
                "('Surfer', 24),"
                "('Suspicious Child', 32),"
                "('Suspicious Lady', 16),"
                "('Suspicious Woman', 140),"
                "('Swimmer', 20),"
                "('Sylveon User', 12),"
                "('Tamer', 47),"
                "('Teacher', 56),"
                "('Team Aqua', 280),"
                "('Team Flare', 210),"
                "('Team Flare Lysandre', 240),"
                "('Team Galactic', 280),"
                "('Team Magma', 280),"
                "('Team Plasma', 213),"
                "('Team Rainbow Rocket', 320),"
                "('Team Rocket', 96),"
                "('Team Skull', 60),"
                "('Tourist', 76),"
                "('Trial Guide', 48),"
                "('Triathlete', 40),"
                "('Tuber', 4),"
                "('Ultra Recon Squad', 12),"
                "('Umbreon User', 200),"
                "('Vaporeon User', 200),"
                "('Veteran', 97),"
                "('Waiter', 40),"
                "('Waitress', 38),"
                "('Worker', 57),"
                "('Young Couple', 84),"
                "('Youngster', 22),"
                "('Youth Athlete', 28)"
               )
    cur.execute("INSERT INTO rank VALUES"
                "('Starter', 5),"
                "('Beginner', 10),"
                "('Amateur', 20),"
                "('Ace', 50),"
                "('Pro', 55),"
                "('Master', 60),"
                "('Champion', 65),"
                "('Rival 1', 5),"
                "('Rival 2', 9),"
                "('Rival 3', 18),"
                "('Rival 4', 20),"
                "('Rival 5', 25),"
                "('Rival 6', 40),"
                "('Rival 7', 53),"
                "('Gym Leader 1', 12),"
                "('Gym Leader 2', 21),"
                "('Gym Leader 3', 24),"
                "('Gym Leader 4', 32),"
                "('Gym Leader 5', 43),"
                "('Gym Leader 6', 50),"
                "('Gym Leader 7', 54),"
                "('Gym Leader 8', 55),"
                "('Elite Four', 59)"
                )
    conn.commit()

if __name__ == '__main__':
  import fire
  fire.Fire()