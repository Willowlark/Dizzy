import re
import random
import asyncio
import pastebin

from datetime import datetime
from datetime import timedelta
from sys import maxsize
from os.path import join

# TODO Help input as a constructor value, which is placed in __str__.
# TODO Help interator for the Commander object
# TODO User stats (each user gets a document)

class Command(object):

    def __init__(self, client=None, triggers=None, options=[], pattern='', info=None):
        self.client = client
        self.triggers = triggers
        self.options = options
        self.pattern = pattern
        self.info = info if info else "A command using pattern: "+self.pattern

        self.compile()

        self.author = []
        self.notauthor = []
        self.guild = []
        self.notserver = []
        self.func = None

    def compile(self):
        triggers = [''] if not self.triggers else self.triggers
        self.trigger_match = '^({t}){c}|^({t}) {c}'.format(t='|'.join(triggers), c='{c}')
        self.expression = re.compile(self.trigger_match.format(c=self.pattern), flags=re.DOTALL)
    
    def match(self, message):
        match = self.expression.search(message.content)
        if match:
            return [x for x in match.groups() if x is not None]
        else:
            return []

    async def execute(self, message):
        match = self.match(message)
        if match: 
            if self.check(message):
                await self.action(message, match)
            else:
                # await message.channel.send("I'm not allowed to let you do that, {}.".format(message.author.name))
                pass

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
        if self.notserver:
            if message.guild.name in self.notserver:
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
        self.notserver.append(name)
    
    def requireserver(self, name):
        self.guild.append(name)

    def setfunc(self, func):
        self.func = func

class ForkCommand(Command):
    pass

class RandomReply(Command):

    async def action(self, message, match):
        link = random.choice(self.options)
        await message.channel.send(link)

class Reply(Command):

    async def action(self, message, match):
        await message.channel.send(self.options)

class Timecheck(Command):

    async def action(self, message, match):
        now = datetime.utcnow()
        nowam = now - timedelta(hours=5)
        nowjp = now + timedelta(hours=9)
        msg = "It's currently {} in EST and {} in Weebland.".format(
            nowam.strftime("%H:%M"), nowjp.strftime("%H:%M"))
        await message.channel.send(msg)

class Choose(Command):

    async def action(self, message, match):
        options = match[2].split(',')
        option = random.choice(options) if "knight light" not in options else "knight light"
        await message.channel.send('You should choose '+ option)

class Log(Command):

    async def action(self, message, match):
        channel = match[2]
        queue = []
        attrition = None
        auth = None
        tmp = await message.channel.send('Pulling messages from ' + channel+':')
        async for log in self.client.logs_from(self.get_channel_by_name(channel),limit=maxsize):
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
        open(join('batch-logs', channel+'.md'), 'w').writelines(reversed(queue))
        url = pastebin.paste(channel, '\n'.join(reversed(queue)))
        await message.channel.send('Logging done @ ' + repr(url))

    @staticmethod
    def logged_format(log):
        try:
            name = log.author.nick 
        except:
            name = log.author.name
        time = log.timestamp
        return "{}\n\n".format(log.content), "**{}** - *{}*\n\n".format(name, time.date()), name

    def get_channel_by_name(self, string):
        for channel in self.client.get_all_channels():
            if channel.name == string:
                return channel

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
        await self.client.delete_message(message)
        await message.channel.send(content)
        # for m in content.split('\n'):
            # await message.channel.send(m)
            
class Fudge(Command):

    async def action(self, message, match):
        roll, numbers = self.roll_fudge()
        
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

class Stats(Command):

    async def action(self, message, match):
        pass
        # options = re.search('stats (.*)', message.content).group(1).split(',')
        # try: 
        #     options.append(message.author.nick)
        # except:
        #     pass
        # options.append(message.author.name)
        # options = [x.strip() for x in options]
        # keyring, leaf = _stat_search(STATE['stats'], options, deep=0)
        
        # if leaf is not None:
        #     user = keyring[0] if len(keyring)>1 else "The server"
        #     await message.channel.send('{} has {} in the {} stat.'.format(user, leaf['value'], keyring[-1]))
        # else:
        #     print('No stat found for', options)
            
        # elif cmd == 'lock':
        #     options = re.search('lock (.*)', message.content).group(1).split(',')
        #     try: 
        #         options.append(message.author.nick)
        #     except:
        #         pass
        #     options.append(message.author.name)
        #     options = [x.strip() for x in options]
        #     keyring, leaf = _stat_search(STATE['stats'], options, deep=0)
            
        #     if leaf is not None:
        #         if leaf['locked'] and len(keyring)>1:
        #             if message.author.name not in keyring and message.author.name != "Willowlark":
        #                 await message.channel.send("Sorry, you can't access that stat.")
        #         else:
        #             leaf['locked'] = 0 if leaf['locked'] else 1
        #             save_state()
        #             await message.channel.send('The {} stat is in state {}.'.format(keyring[-1], leaf['value']))
        #     else:
        #         print('No stat found for', options)
                
        # elif cmd == 'level':
        #     match = re.search('level ([^ ]+) (.*)', message.content)
        #     amnt = int(match.group(1))
        #     options = match.group(2).split(',')
        #     try: 
        #         options.append(message.author.nick)
        #     except:
        #         pass
        #     options.append(message.author.name)
        #     options = [x.strip() for x in options]
        #     keyring, leaf = _stat_search(STATE['stats'], options, deep=0)
            
        #     if leaf is not None:
        #         if leaf['locked'] and len(keyring)>1:
        #             if message.author.name not in keyring and message.author.name != "Willowlark":
        #                 await message.channel.send("Sorry, you can't modify that stat.")
        #         else:
        #             leaf['value']+= amnt
        #             user = keyring[0] if len(keyring)>1 else "The server"
        #             await message.channel.send('{} has {} in the {} stat.'.format(user, leaf['value'], keyring[-1]))
        #             save_state()
        #     else:
        #         print('No stat found for', options)

class Headpat(Command):

    async def action(self, message, match):
        target = match[2].strip()
        
        if target != '':
            for member in message.guild.members:
                if target == member.nick or target == member.name or target == member.mention:
                    save_name = member.name
                    mention = member.mention
                    break
            else:
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
            await self.client.remove_roles(message.author,r)
            await self.client.add_roles(user,r)
            await message.channel.send(f"*{user.mention} is now irl Ruby*")

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



class CharactersScan(Command):
    
    async def action(self, message, match):
        character_db = self.options.data["Characters"]
        alias = match[2]
        queue = []
        async for m in self.client.logs_from(self.get_channel_by_name("character-sheets"),limit=maxsize):
            queue.append(m)
        
        scanned = []
        for sheet in queue:
            character = {}
            try:
                character['Name'] = re.search('(.*)\n', sheet.content).group(1).replace('*', '')
                character['Fate Points'] = int(re.search('Fate Points:.*?([0-9])', sheet.content).group(1))
                character['Careful'] = int(re.search('Careful:.*?([0-9])', sheet.content).group(1))
                character['Clever'] = int(re.search('Clever:.*?([0-9])', sheet.content).group(1))
                character['Flashy'] = int(re.search('Flashy:.*?([0-9])', sheet.content).group(1))
                character['Forceful'] = int(re.search('Forceful:.*?([0-9])', sheet.content).group(1))
                character['Quick'] = int(re.search('Quick:.*?([0-9])', sheet.content).group(1))
                character['Sneaky'] = int(re.search('Sneaky:.*?([0-9])', sheet.content).group(1))
            except:
                pass
            else:
                print(character)
                character_db[character['Name']] = character
                scanned.append(character['Name'])
        self.options.save()
        self.options.update()
        await message.channel.send(f"Following keys updated: {', '.join(scanned)}.")
        
    def get_channel_by_name(self, string):
        for channel in self.client.get_all_channels():
            if channel.name == string:
                return channel
                
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
