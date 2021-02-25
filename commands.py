import re
import random
import asyncio
import arrow
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from sys import maxsize
from os.path import join

import rollparser

# CRIT: MATCH[0] IS THE STRING, MATCH[1] IS THE TRIGGER, MATCH[2] STARTS THE USER INPUT!!!!!!!

# TODO Help input as a constructor value, which is placed in __str__.
# TODO Help interator for the Commander object

# FIXME: The way the compile works for commands, the trigger is only appended to the front. This prevents use of OR statements that join two completely distinct commands

class Command(object):

    def __init__(self, triggers=None, options=[], options_source=None, pattern='', info=None, author=None, update_me=False):
        self.triggers = triggers
        self.options = options
        self.options_source = options_source
        self.pattern = pattern
        self.info = info if info else "A command using pattern: "+self.pattern

        self.compile()

        self.author = author
        self.update_me=update_me
        self.func = None

    def compile(self):
        triggers = [''] if not self.triggers else self.triggers
        triggers = [triggers] if type(triggers) == str else self.triggers
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
        pass

    def check(self, message):
        
        # Author must/not
        if self.author:
            if message.author.name != self.author:
                return False

        # Lambda 
        if self.func:
            if not self.func(message): 
                return False
        
        return True

    def setfunc(self, func):
        self.func = func

class RandomReply(Command):

    async def action(self, message, match):
        link = random.choice(self.options.REPLY)
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
        option = random.choice(options)
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
        await message.channel.send('Logging done')

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
                
        self.options = self.options.append(pd.Series({'ID':self.options['ID'].max()+1, 'PATTER':message.author.name, 'USER_TARGET':save_name, 'MODIFIED_BIT':True}), ignore_index=True)
        pat_count = self.options[self.options['USER_TARGET'] == save_name]['USER_TARGET'].count()
            
        await message.channel.send(f"*{message.author.mention} headpats {mention}*")
        if save_name != 'Dizzy':
            await message.channel.send(f"{mention} has been headpatted {pat_count} times.")
        else:
            await message.channel.send(f"{message.author.mention} is so nice <3")

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

class _RFAMode(Command):
    
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

class _RFAMembership(Command):
    
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

class CounterBase(Command):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tier = 'Server'
        
    def tier_check(self, op):
        if op == 'counter':
            return "Server"
        elif op == 'mycounter':
            return "User"
        elif op == 'globalcounter':
            return "Global"
    
    def target_index_search(self, message, tier, counter_matches):
        
        target_index = None
        for index, row in counter_matches.iterrows():
            if row['TIER'] == 'User' and tier == 'User':
                if row['CREATOR'] == message.author.name:
                    target_index = index
            elif row['TIER'] == 'Server' and tier == 'Server':
                if row['SERVER_NAME'] == message.guild.name:
                    target_index = index
            elif row['TIER'] == 'Global' and tier == 'Global':
                target_index = index
            
        return target_index

class CounterIncrement(CounterBase):

    async def action(self, message, match):
        command, op, target, amnt = match[1:]
        amnt = int(amnt)
        
        tier = self.tier_check(command)

        counter_matches = self.options[self.options['COUNTER_NAME'] == target]
        
        target_index = self.target_index_search(message, tier, counter_matches)

        if target_index is None:
            await message.channel.send("I'm not counting those right now.")
        elif op == 'add':
            self.options.loc[self.options.index==target_index, 'CNT']+=amnt
            self.options.loc[self.options.index==target_index, 'MODIFIED_BIT'] = True
            result = int(self.options.loc[self.options.index==target_index, 'CNT'])
            await message.channel.send(f"The **{target}** count is {result}.")
        elif op == 'sub':
            self.options.loc[self.options.index==target_index, 'CNT']-=amnt
            self.options.loc[self.options.index==target_index, 'MODIFIED_BIT'] = True
            result = int(self.options.loc[self.options.index==target_index, 'CNT'])
            await message.channel.send(f"The **{target}** count is {result}.")
    
class CounterCheck(CounterBase):
    
    async def action(self, message, match):
        command, op, target = match[1:]
        
        tier = self.tier_check(command)
        
        counter_matches = self.options[self.options['COUNTER_NAME'] == target]
        
        target_index = self.target_index_search(message, tier, counter_matches)

        if target_index is None:
            await message.channel.send("I'm not counting those right now.")
        else:
            result = int(self.options.loc[self.options.index==target_index, 'CNT'])
            await message.channel.send(f"The **{target}** count is {result}.")

class CounterSet(CounterBase):

    async def action(self, message, match):
        command, op, target, amnt = match[1:]
        amnt = int(amnt)
        
        tier = self.tier_check(command)
        
        counter_matches = self.options[self.options['COUNTER_NAME'] == target]
        
        target_index = self.target_index_search(message, tier, counter_matches)

        if target_index is None:
            idd = self.options['ID'].max()+1 if self.options['ID'].max() is not np.nan else 1
            x = {
                'ID': idd,
                'TIER': tier,
                'SERVER_NAME': message.guild.name,
                'CREATOR': message.author.name,
                'COUNTER_NAME': target,
                'CNT': amnt,
                'MODIFIED_BIT': True
            }
            x = pd.Series(x)
            self.options = self.options.append(x, ignore_index=True)
            target_index = self.options.index[-1]
        else:
            self.options.loc[self.options.index==target_index, 'CNT'] = amnt
            self.options.loc[self.options.index==target_index, 'MODIFIED_BIT'] = True
        
        result = int(self.options.loc[self.options.index==target_index, 'CNT'])
        await message.channel.send(f"The **{target}** count is now {result}!")

class CounterRemove(CounterBase):

    async def action(self, message, match):
        command, op, target = match[1:]
        
        tier = self.tier_check(command)
        
        counter_matches = self.options[self.options['COUNTER_NAME'] == target]
        
        target_index = self.target_index_search(message, tier, counter_matches)

        if target_index is None:
            await message.channel.send("I'm not counting those right now.")
        else:
            self.options.loc[self.options.index==target_index, 'RM'] = True
            await message.channel.send("No longer counting {}!".format(target))

class CounterList(CounterBase):

    async def action(self, message, match):
        matches = match[1:]
        if len(matches) == 3:
            command, op, allflag = matches
        elif len(matches) == 2:
            command, op = matches
            allflag = None
            
        tier = self.tier_check(command)
        
        lines = ["Here's what I have.\n", '```']
        series_lines = pd.Series()
        for index, row in self.options.iterrows():
            if row['TIER'] == 'User' and (tier == 'User' or allflag):
                if row['CREATOR'] == message.author.name:
                    series_lines = series_lines.append(pd.Series([row['CNT']], index=[row['COUNTER_NAME']]))
            elif row['TIER'] == 'Server' and (tier == 'Server' or allflag):
                if row['SERVER_NAME'] == message.guild.name:
                    series_lines = series_lines.append(pd.Series([row['CNT']], index=[row['COUNTER_NAME']]))
            elif row['TIER'] == 'Global' and (tier == 'Global' or allflag):
                series_lines = series_lines.append(pd.Series([row['CNT']], index=[row['COUNTER_NAME']]))
        
        lines.append(series_lines.to_string())
        lines.append('```')

        await message.channel.send("".join(lines))

class QuestionPlease(Command):
    
    async def action(self, message, match):
        # import IPython; IPython.embed()
        row = self.options[self.options.DONE == 0].sample().iloc[0]

        await message.channel.send(f"Here's the Question!\n**{row['QUESTION']}**\n\n:one: {row['OPTION_1']}\n:two: {row['OPTION_2']}")
        
        self.options.loc[self.options.ID==row.ID, 'DONE'] = 1
        self.options.loc[self.options.ID==row.ID, 'MODIFIED_BIT'] = True

class FateAccelLoad(Command):
    
    async def action(self, message, match):
        # import IPython; IPython.embed()
        character = {}
        try:
            character['CHARACTER_NAME'] = re.search('^\*\*(.*?)\*\*', match[3]).group(1)#.replace('*', '')
            character['CHARACTER_SHORT_NAME'] = match[2]
            character['DEFAULT_DIE_CODE'] = '4dF'
            character['FATE_POINTS'] = int(re.search('\*\*Fate Points:\*\* *([0-9]+)', match[3]).group(1))
            
            s = re.search('\*\*Stress:\*\*((?: *\[.\])+)', match[3]).group(1).strip()
            character['STRESS'] = len([x for x in s[1:-1].split('] [') if x != ' '])
            character['CONSEQUENCE_2'] = re.search('2  Mild:(.*)\n', match[3]).group(1).strip()
            character['CONSEQUENCE_4'] = re.search('4  Moderate:(.*)\n', match[3]).group(1).strip()
            character['CONSEQUENCE_6'] = re.search('6  Severe:(.*)\n', match[3]).group(1).strip()
            
            s = re.search('\*\*Aspects\*\*((?:\n+\* .*)+)', match[3]).group(1).strip()
            character['ASPECT_1'], character['ASPECT_2'], character['ASPECT_3'], character['ASPECT_4'], character['ASPECT_5'] = [x.strip() for x in ''.join(s.split('*')).split('\n')]
            character['CAREFUL'] = int(re.search('Careful: *`([+-]?[0-9])`', match[3]).group(1))
            character['CLEVER'] = int(re.search('Clever: *`([+-]?[0-9])`', match[3]).group(1))
            character['FLASHY'] = int(re.search('Flashy: *`([+-]?[0-9])`', match[3]).group(1))
            character['FORCEFUL'] = int(re.search('Forceful: *`([+-]?[0-9])`', match[3]).group(1))
            character['QUICK'] = int(re.search('Quick: *`([+-]?[0-9])`', match[3]).group(1))
            character['SNEAKY'] = int(re.search('Sneaky: *`([+-]?[0-9])`', match[3]).group(1))
            
            idd = self.options['ID'].max()+1 if self.options['ID'].max() is not np.nan else 1
            character['ID'] = idd
            character['SERVER'] = message.guild.name
            character['MODIFIED_BIT'] = True
            
        except:
            await message.channel.send(f"I'm sorry, I didn't quite get that (T.T)")
        else:
            print(character)
            self.options = self.options.append(character,ignore_index=True)
            await message.channel.send(f"Following character updated: `{match[2]}`.")

class FateAccelCheck(Command):
    
    async def action(self, message, match):
        alias = match[2]
        row = self.options[self.options['CHARACTER_SHORT_NAME'] == alias]
        if not row.empty:
            row = row.iloc[0]
            if row['SERVER'] == message.guild.name:
                stress =('[x] '*row['STRESS']+'[ ] '*(3-row['STRESS'])).strip()
                character_string = f"**{row['CHARACTER_NAME']}**\n\n**Fate Points:** {row['FATE_POINTS']}\n**Stress:** {stress}\n**Consequences:**\n2  Mild: {row['CONSEQUENCE_2']}\n4  Moderate: {row['CONSEQUENCE_4']}\n6  Severe: {row['CONSEQUENCE_6']}\n\n**Aspects**\n\n* {row['ASPECT_1']}\n* {row['ASPECT_2']}\n* {row['ASPECT_3']}\n* {row['ASPECT_4']}\n* {row['ASPECT_5']}\n\n**Approaches**\nCareful: `{row['CAREFUL']}`\nClever: `{row['CLEVER']}`\nFlashy: `{row['FLASHY']}`\nForceful: `{row['FORCEFUL']}`\nQuick: `{row['QUICK']}`\nSneaky: `{row['SNEAKY']}`"
                
                if len(match)==4: character_string = f"```{character_string}\n```"
                else: character_string = f">>> {character_string}"
                
                await message.channel.send(f"{alias}'s Character Sheet is as follows!\n{character_string}")
            else:
                await message.channel.send(f"{alias} isn't a Character I know, can you introduce me sometime? (^^)")
        else:
            await message.channel.send(f"{alias} isn't a Character I know, can you introduce me sometime? (^^)")

class CharacterList(Command):
    
    async def action(self, message, match):
        li = self.options[self.options['SERVER'] == message.guild.name][['CHARACTER_SHORT_NAME', 'CHARACTER_NAME']].rename(columns={'CHARACTER_SHORT_NAME':"Alias"}).set_index('Alias')
        await message.channel.send(f"I have the character sheets for these characters!\n ```{li}```")

class CharacterRoll(Command):
    
    async def action(self, message, match):
        alias = match[2]
        key = match[3]
        skey = re.sub(r'\w+', lambda m:m.group(0).upper(), key).replace(' ', '_')
        row = self.options[self.options['CHARACTER_SHORT_NAME'] == alias]
        if not row.empty:
            row = row.iloc[0]
            if row['SERVER'] == message.guild.name:
                value = row[skey]
                
                if type(value) == np.int64:
                    og, rolls, unmod = rollparser.parse(row['DEFAULT_DIE_CODE'])
                    total = value+unmod
                    m = f"{row['CHARACTER_SHORT_NAME']} rolled **{unmod}** *{rolls}*!\n\n Their `{key}` stat is **{value}**, so total is {unmod}+{value}=**{total}**!"
                    await message.channel.send(m)
                else:
                    try:
                        og, rolls, total = rollparser.parse(value)
                    except: 
                        await message.channel.send(f"How do I roll that?! XT")
                    else:
                        await message.channel.send(f"{row['CHARACTER_SHORT_NAME']} rolled `{og}` and got {total}!\nThe rolls were :*{rolls}*")
        else:
            await message.channel.send(f"I don't know if {alias} can do that...")

class CharacterMod(Command):
    
    async def action(self, message, match):
        alias = match[2]
        key = match[3]
        value = match[4]
        skey = re.sub(r'\w+', lambda m:m.group(0).upper(), key).replace(' ', '_')
        # import IPython; IPython.embed()
        row = self.options[self.options['CHARACTER_SHORT_NAME'] == alias]
        if not row.empty:
            row = row.iloc[0]
            if row['SERVER'] == message.guild.name:
                
                try: 
                    if self.options.dtypes[skey] == np.int64: value = int(value)
                    if self.options.dtypes[skey] == object: value = str(value)
                except ValueError:
                    await message.channel.send(f"I don't think that's what goes in that category...")
                else:
                    old_value = row[skey]
                    self.options.loc[self.options.index==row.name, skey] = value
                    self.options.loc[self.options.index==row.name, 'MODIFIED_BIT'] = True
                    await message.channel.send(f"{row['CHARACTER_SHORT_NAME']} had {old_value} in {key}, I changed it to {value}.")
            else:
                await message.channel.send(f"{alias} doesn't have that...")
        else:
            await message.channel.send(f"{alias} doesn't have that...")

REFERENCE = {
    'Command' : Command,
    'RandomReply' : RandomReply,
    'Reply' : Reply,
    'Timecheck' : Timecheck,
    'Choose' : Choose,
    'Log' : Log,
    'Stab' : Stab,
    'Refresh' : Refresh,
    'Ghost' : Ghost,
    'Fudge' : Fudge,
    'Roll' : Roll,
    'Headpat' : Headpat,
    'IrlRuby' : IrlRuby,
    # 'RFAMode' : RFAMode,
    # 'RFAMembership' : RFAMembership,
    'CounterIncrement' : CounterIncrement,
    'CounterCheck' : CounterCheck,
    'CounterSet' : CounterSet,
    'CounterRemove' : CounterRemove,
    'CounterList' : CounterList,
    'QuestionPlease' : QuestionPlease,
    'FateAccelLoad' : FateAccelLoad,
    'FateAccelCheck' : FateAccelCheck,
    'CharacterList' : CharacterList,
    'CharacterRoll' : CharacterRoll,
    'CharacterMod' : CharacterMod
}