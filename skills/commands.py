import re
import random
import asyncio
import pastebin
import arrow
import rollparser

from datetime import datetime
from datetime import timedelta
from sys import maxsize
from os.path import join

# CRIT: MATCH[0] IS THE STRING, MATCH[1] IS THE TRIGGER, MATCH[2] STARTS THE USER INPUT!!!!!!!

# TODO Help input as a constructor value, which is placed in __str__.
# TODO Help interator for the Commander object
# TODO User stats (each user gets a document)

class Command(object):

    def __init__(self, triggers=None, options=[], pattern='', info=None):
        self.triggers = triggers
        self.options = options
        self.pattern = pattern
        self.info = info if info else "A command using pattern: "+self.pattern

        self.compile()

        self.author = []
        self.notauthor = []
        self.guild = []
        self.notguild = []
        self.func = None

    def compile(self):
        triggers = [''] if not self.triggers else self.triggers
        #TODO Accomodate | in this pattern.
        self.trigger_match = '^({t}){c}|^({t}) {c}'.format(t='|'.join(triggers), c='{c}') 
        self.expression = re.compile(self.trigger_match.format(c=self.pattern), flags=re.DOTALL)
    
    def match(self, message):
        match = self.expression.match(message.content)
        if match:
            return [x for x in match.groups() if x is not None]
        else:
            return []

    async def execute(self, message):
        match = self.match(message)
        if match: 
            if self.check(message):
                await self.action(message, match)
                return True
            else:
                # await message.channel.send("I'm not allowed to let you do that, {}.".format(message.author.name))
                return False

    async def action(self, message, match):
        await asyncio.sleep(10)
        await message.channel.send('Waited!')

    def check(self, message):
        
        # Author must/not
        if self.author:
            if message.author.name not in self.author:
                return False
        if self.notauthor:
            if message.author.name in self.notauthor:
                return False
                
        # Server must/not
        if self.guild:
            if message.guild.name not in self.guild:
                return False
        if self.notguild:
            if message.guild.name in self.notguild:
                return False

        # Lambda 
        if self.func:
            if not self.func(message): 
                return False
        
        return True

    def banauthor(self, name):
        self.notauthor.append(name)
    
    def requireauthor(self, name):
        self.author.append(name)
        
    def banserver(self, name):
        self.notguild.append(name)
    
    def requireserver(self, name):
        self.guild.append(name)

    def setfunc(self, func):
        self.func = func

class RandomReply(Command):

    async def action(self, message, match):
        link = random.choice(self.options)
        await message.channel.send(link)

class Reply(Command):

    async def action(self, message, match):
        await message.channel.send(self.options)

class Timecheck(Command):

    async def action(self, message, match):
        now = arrow.now()
        nowam = now.to('America/New_York')
        nowjp = now.to('Asia/Tokyo')
        msg = "It's currently {} in EST\n and {} in Weebland.".format(
            nowam.format("dddd, MMM D h:mm A YYYY"), nowjp.format('dddd, MMM D h:mm A YYYY'))
        await message.channel.send(msg)

class Choose(Command):

    async def action(self, message, match):
        options = match[2].split(',')
        options = [op.strip() for op in options]
        option = random.choice(options) if "knight light" not in options else "knight light"
        await message.channel.send('You should choose '+ option)

class Log(Command):

    async def action(self, message, match):
        channel = match[2]
        queue = []
        attrition = None
        auth = None
        tmp = await message.channel.send('Pulling messages from ' + channel+':')
        async for log in message.channel.history(limit=maxsize):
            log, name, who = self.logged_format(log)
            if auth is None:
                auth = who
                attrition = name
            elif auth != who:
                queue.append(attrition)
                auth = who
                attrition = name
            queue.append(log)
        queue.append(attrition)
        # TODO use makedirs here
        open(join('DizzyHoG/batch-logs', channel+'.md'), 'w').writelines(reversed(queue))
        url = pastebin.paste(channel, '\n'.join(reversed(queue)))
        await message.channel.send('Logging done @ ' + repr(url))

    @staticmethod
    def logged_format(log):
        try:
            name = log.author.nick 
        except:
            name = log.author.name
        time = log.created_at
        return "{}\n\n".format(log.content), "**{}** - *{}*\n\n".format(name, time.date()), name

class Stab(Command):

    async def action(self, message, match):
        who = random.choice([x for x in list(message.guild.members) if x.name != "Dizzy"])
        who = who.nick if who.nick else who.name
            
        # who = who.mention
        what = random.choice(['shanks', 'stabs'])
        
        act = '*{} {}!*'.format(what, who) if random.randint(1,10) != 1 else '*attempts to {} {}; but trips and stabs herself instead*!'.format(what, who)
        
        if message.author.name == "Halim": # Create the fork command for this.
            await message.channel.send("Stop making me do this...")
        else:
            await message.channel.send(act)

class Refresh(Command):

    async def action(self, message, match):
        # await message.channel.send("I'll go reread my notes!")
        dbs = self.options[0]
        for db in dbs:
            dbs[db].update()
        
        print(dbs['Local'].data['Counters'])
        
        await message.channel.send("All set!")

class Ghost(Command):

    async def action(self, message, match):
        content = match[2]
        await message.delete()
        await message.channel.send(content)
        # for m in content.split('\n'):
            # await message.channel.send(m)

class Fudge(Command):

    async def action(self, message, match):
        roll, numbers = self.roll_fudge()
        if len(match)>2:
            modifier = int(match[2])
            await message.channel.send(f"You rolled *{numbers}*  with a modifier of *{modifier}*  for a total of **{roll+modifier}** !")
        else:
            await message.channel.send(f"You rolled *{numbers}*  for a total of **{roll}** !")
            
    @staticmethod
    def roll_fudge():
        sides = [-1, -1, 0, 0, 1, 1]
        rolls = []
        tote = 0
        for x in range(0, 4):
            roll = sides[random.randint(0, 5)]
            rolls.append(roll)
            tote+=roll
        return tote, rolls

class Roll(Command):

    async def action(self, message, match):
        og, rolls, total = rollparser.parse(match[2])
        await message.channel.send(f"Rolled `{og}` and got {total}!\nThe rolls were :*{rolls}*")
            


class Headpat(Command):

    async def action(self, message, match):
        target = match[2].strip()
        m_check = re.match('<@!?([0-9]+)>', target)
        if m_check is not None:
            target = m_check.group(1)
        
        if target != '':
            for member in message.guild.members:
                opts = [member.nick, member.name,re.match('<@!?([0-9]+)>', member.mention).group(1)]
                if target in opts:
                    save_name = member.name
                    mention = member.mention
                    break
            else:
                # await message.channel.send(f"I don't know who {member.nick}, {member.name} or {member.mention} is :(")
                return None
        else:
            save_name = 'Dizzy'
            mention = 'Dizzy'
        
        FRENS = self.options.data['Headpats']
        
        if save_name not in FRENS:
            value = 1
            FRENS[save_name] = 1
        else:
            value = FRENS[save_name]+1
            FRENS[save_name]+=1
            
        await message.channel.send(f"*{message.author.mention} headpats {mention}*")
        if save_name != 'Dizzy':
            await message.channel.send(f"{mention} has been headpatted {value} times.")
        else:
            await message.channel.send(f"{message.author.mention} is so nice <3")
        self.options.save()
        self.options.update()

class IrlRuby(Command):

    async def action(self, message, match):
        target = match[2].strip()
        
        if target != '':
            for member in message.guild.members:
                if target == member.nick or target == member.name or target == member.mention:
                    save_name = member.name
                    mention = member.mention
                    user = member
                    break
            else:
                return None
        else:
            return None
        
        if 'irl Ruby' in [x.name for x in message.author.roles]:
            r = [x for x in message.author.roles if x.name == 'irl Ruby'][0]
            await message.author.remove_roles(r)
            await user.add_roles(r)
            await message.channel.send(f"*{user.mention} is now irl Ruby*")

class RFAMode(Command):
    
    async def action(self, message, match):
        target, op = match[2:]
        if target in [x.name for x in message.guild.text_channels]:
            CHANNELS = self.options.data['RFA']['Channels']
            
            
            if op.lower() == 'true':
                if target not in CHANNELS:
                    CHANNELS[target] = {"Enabled": 'true', "Members": [], "Name":target}
                else:
                    CHANNELS[target]['Enabled'] = 'true'
                
                await message.channel.send(f"RFA mode is now set to `{op.lower()}` for `{target}`.")
            elif op.lower() == 'false' and target in CHANNELS:
                CHANNELS[target]['Enabled'] = 'false'
                await message.channel.send(f"RFA mode is now disabled for `{target}`.")
            else:
                print("Don't know what to do with that operation.")
        
        self.options.save()
        self.options.update()

class RFAMembership(Command):
    
    async def action(self, message, match):
        rfa, target = match[2:]
            
        for member in message.guild.members:
            if target == member.nick or target == member.name or target == member.mention:
                save_name = member.name
                mention = member.mention
                break
            
        RFA = self.options.data['RFA']["Channels"][rfa]['Members']
        
        channel = [x for x in message.guild.text_channels if x.name == rfa][0]
        if save_name not in RFA:
            RFA.append(save_name)
            await channel.send(f"*Welcome to the RFA {mention}.*")
        else:
            RFA.remove(save_name)
            await channel.send(f"*{mention} has left the RFA.*")
            
        online = []
        for user in RFA:
            for member in message.guild.members:
                if member.name == user and str(member.status) == 'online':
                    online.append(member.nick if member.nick is not None else member.name)
        await channel.edit(topic=', '.join(online))
        
        self.options.save()
        self.options.update()

class CounterIncrement(Command):

    async def action(self, message, match):
        op, target, amnt = match[2:]
        amnt = int(amnt)
        COUNTERS = self.options.data['Counters']

        if target not in COUNTERS:
            await message.channel.send("I'm not counting those right now.")
        else:
            value = COUNTERS[target]
            if op == "add":
                COUNTERS[target]+=amnt
                await message.channel.send("The {} count is now {}!".format(target, COUNTERS[target]))
            elif op == "sub":
                COUNTERS[target]-=amnt
                await message.channel.send("The {} count is now {}!".format(target, COUNTERS[target]))
            else:
                await message.channel.send("I don't know how to do that, sorry.")
        self.options.save()
        self.options.update()

class CounterCheck(Command):
    
    async def action(self, message, match):
        op, target = match[2:]
        COUNTERS = self.options.data['Counters']

        if target not in COUNTERS:
            await message.channel.send("I'm not counting those right now.")
        else:
            await message.channel.send("The {} count is {}.".format(target, COUNTERS[target]))

class CounterSet(Command):

    async def action(self, message, match):
        op, target, amnt = match[2:]
        amnt = int(amnt)
        COUNTERS = self.options.data['Counters']

        COUNTERS[target] = amnt
        
        await message.channel.send("The {} count is now {}!".format(target, COUNTERS[target]))
        
        self.options.save()
        self.options.update()

class CounterRemove(Command):

    async def action(self, message, match):
        target = match[3]
        COUNTERS = self.options.data['Counters']

        if target not in COUNTERS:
            await message.channel.send("I'm not counting those right now.")
        else:
            del COUNTERS[target]
            await message.channel.send("No longer counting {}!".format(target))
        
        self.options.save()
        self.options.update()

class CounterList(Command):

    async def action(self, message, match):
        
        COUNTERS = self.options.data['Counters']

        lines = ["Here's what I have.\n", '```']
        for key, value in COUNTERS.items():
            if key[0] != '_':
                lines.append("{} count is at {}.\n".format(key, value))
        lines.append('```')

        await message.channel.send("".join(lines))

class QuestionPlease(Command):
    
    async def action(self, message, match):
        QUESTIONS = self.options.data['Questions']["Questions"]
        cnt = len(QUESTIONS)
        while 1:
            roll = random.randint(0, cnt-1)
            QUESTION = QUESTIONS[roll]
            if not QUESTION['done']: break
        
        await message.channel.send(f"Here's the Question!\n**{QUESTION['question']}**\n\n:one: {QUESTION['option1']}\n:two: {QUESTION['option2']}")
        
        QUESTION['done'] = True
        
        self.options.save()
        self.options.update()



class CharacterLoad(Command):
    
    async def action(self, message, match):
        character_db = self.options.data["Characters"]

        character = {}
        try:
            character['Name'] = re.search('(.*)\n', match[3]).group(1).replace('*', '')
            character['Fate Points'] = int(re.search('Fate Points:.*?([0-9])', match[3]).group(1))
            character['Careful'] = int(re.search('Careful:.*?([0-9])', match[3]).group(1))
            character['Clever'] = int(re.search('Clever:.*?([0-9])', match[3]).group(1))
            character['Flashy'] = int(re.search('Flashy:.*?([0-9])', match[3]).group(1))
            character['Forceful'] = int(re.search('Forceful:.*?([0-9])', match[3]).group(1))
            character['Quick'] = int(re.search('Quick:.*?([0-9])', match[3]).group(1))
            character['Sneaky'] = int(re.search('Sneaky:.*?([0-9])', match[3]).group(1))
        except:
            pass
        else:
            print(character)
            character_db[match[2]] = character
        self.options.save()
        self.options.update()
        await message.channel.send(f"Following keys updated: `{match[2]}`.")

class CharacterCheck(Command):
    
    async def action(self, message, match):
        character_db = self.options.data["Characters"]
        alias = match[2]
        key = match[3]
        key = re.sub(r'\w+', lambda m:m.group(0).capitalize(), key)
        print(key)
        
        if key in character_db[alias]:
            value = character_db[alias][key]
            name = character_db[alias]['Name']
            await message.channel.send(f"{name} ({alias}) has a {value} in {key}.")
        else:
            await message.channel.send(f"{alias} doesn't have that...")

class CharacterList(Command):
    
    async def action(self, message, match):
        character_db = self.options.data["Characters"]
        entries = ["Alias : Character Name"]
        for character in character_db:
            entries.append(f"{character} : {character_db[character]['Name']}")
        
        entries = ',\n'.join(entries)
        await message.channel.send("I have the character sheets for these characters!\n ```{}```".format(entries))

class CharacterRoll(Command):
    
    async def action(self, message, match):
        character_db = self.options.data["Characters"]
        alias = match[2]
        key = match[3]
        key = re.sub(r'\w+', lambda m:m.group(0).capitalize(), key)
        
        if key in character_db[alias]:
            value = character_db[alias][key]
            name = character_db[alias]['Name']
            
            roll, numbers = self.roll_fudge()
            total = value+roll
            m = f"{name} ({alias}) rolled **{roll}** *{numbers}*!\n\n Their `{key}` stat is **{value}**, so total is {roll}+{value}=**{total}**!"
            await message.channel.send(m)
            if roll == -4:
                await message.channel.send("...oof.")
        else:
            await message.channel.send(f"{alias} doesn't have that...")

    @staticmethod
    def roll_fudge():
        sides = [-1, -1, 0, 0, 1, 1]
        rolls = []
        tote = 0
        for x in range(0, 4):
            roll = sides[random.randint(0, 5)]
            rolls.append(roll)
            tote+=roll
        return tote, rolls

class CharacterMod(Command):
    
    async def action(self, message, match):
        character_db = self.options.data["Characters"]
        alias = match[2]
        key = match[3]
        value = int(match[4])
        key = re.sub(r'\w+', lambda m:m.group(0).capitalize(), key)
        
        if key in character_db[alias]:
            old_value = character_db[alias][key]
            name = character_db[alias]['Name']
            character_db[alias][key] = value
            self.options.save()
            self.options.update()
            await message.channel.send(f"{name} ({alias}) had {old_value} in {key}, I changed it to {value}.")
        else:
            await message.channel.send(f"{alias} doesn't have that...")
