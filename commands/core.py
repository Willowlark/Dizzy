import re
import random
import arrow
import pandas as pd
from sys import maxsize
from os.path import join
import emoji
from sys import modules
from inspect import getmembers, isclass
import commands.rollparser as rollparser

# CRIT: MATCH[0] IS THE STRING, MATCH[1] IS THE TRIGGER, MATCH[2] STARTS THE USER INPUT!!!!!!!

# FIXME: The way the compile works for commands, the trigger is only appended to the front. This prevents use of OR statements that join two completely distinct commands

class Command(object):

    def __init__(self, triggers=None, options=[], options_source=None, pattern='', info=None, author=None, server=None, update_me=False):
        self.triggers = triggers
        self.options = options
        self.options_source = options_source
        self.pattern = pattern
        self.info = info if info else "A command using pattern: "+self.pattern

        self.compile()

        self.author = author
        self.server = server
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

        if self.server:
            if message.guild.id != self.server:
                return False

        # Lambda 
        if self.func:
            if not self.func(message): 
                return False
        
        return True

    def setfunc(self, func):
        self.func = func

class Help(Command):
    
     async def action(self, message, match):
                 
        relevant = self.options.query(f'SERVER_ID == 1 or UID == {message.guild.id}')
        response = []
        longest = 0
        
        for i, row in relevant.iterrows():
            m = row.HELP
            if not m:
                continue
            nls = m.split('\n')
            for x in nls:
                s = x.split(':')
                if len(s[0].strip()) > longest:
                    longest = len(s[0].strip())
                response.append([_.strip() for _ in s])
        
        response = [[f'**{x[0]}**', x[1]] for x in response]
        final_response = []
        rpart = ''
        for x in response:
            if len(rpart) + len('\n    '.join(x)) > 2000:
                final_response.append(rpart+'')
                rpart = ''
            rpart = rpart + '\n    '.join(x)+'\n'
        final_response.append(rpart+'')
        
        await message.channel.send("Here's all the things I can do! (^^)")
        for x in final_response:
            await message.channel.send(x)

class RandomReply(Command):

    async def action(self, message, match):
        link = random.choice(self.options.REPLY)
        await message.channel.send(link)

class Reply(Command):

    async def action(self, message, match):
        emojis_used = re.findall(':\w+?::', self.options)
        m = await message.channel.send(self.options)
        for x in emojis_used:
            await m.add_reaction(emoji.emojize(x[:-1], use_aliases=True))

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

class QuestionPlease(Command):
    
    async def action(self, message, match):
        # import IPython; IPython.embed()
        row = self.options[self.options.DONE == 0].sample().iloc[0]

        await message.channel.send(f"Here's the Question!\n**{row['QUESTION']}**\n\n:one: {row['OPTION_1']}\n:two: {row['OPTION_2']}")
        
        self.options.loc[self.options.ID==row.ID, 'DONE'] = 1
        self.options.loc[self.options.ID==row.ID, 'MODIFIED_BIT'] = True

class TarotDraw(Command):
    
    async def action(self, message, match):
        # import IPython; IPython.embed()
        if len(match) == 2:
            cnt = 1
            rank = None
        elif len(match) == 3:
            if match[2].strip().isdigit():
                cnt = int(match[2])
                rank = None
            else:
                rank = match[2].strip().lower()
        elif len(match) == 4:
            cnt = int(match[2])
            rank = match[3].strip().lower()
        
        if rank:
            opts = self.options[self.options.RANK == rank]
        else:
            opts = self.options
        opts = opts[opts.DRAWN == 0]
        drawn = opts.sample(cnt)
        
        reply = ["I drew:"]
        for i, r in drawn.iterrows():
            pos = 'UPRIGHT' if random.randint(0,1) else 'REVERSED'
            x = f"The {r.RANK.capitalize()} Arcana {r.CARD} {pos}, which means *{r[pos]}*."
            reply.append(x)
            # self.options.loc[self.options.ID==r.ID, 'DRAWN'] = 1
            self.options.loc[self.options.ID==r.ID, 'MODIFIED_BIT'] = True
        
        await message.channel.send('\n'.join(reply))


# REFERENCE = {
#     'Command' : Command,
#     'Help' : Help,
#     'RandomReply' : RandomReply,
#     'Reply' : Reply,
#     'Timecheck' : Timecheck,
#     'Choose' : Choose,
#     'Log' : Log,
#     'Stab' : Stab,
#     'Refresh' : Refresh,
#     'Ghost' : Ghost,
#     'Fudge' : Fudge,
#     'Roll' : Roll,
#     'Headpat' : Headpat,
#     'IrlRuby' : IrlRuby,
#     # 'RFAMode' : RFAMode,
#     # 'RFAMembership' : RFAMembership,
#     'QuestionPlease' : QuestionPlease,
#     'TarotDraw': TarotDraw
# }

clsmembers = getmembers(modules[__name__], isclass)
REFERENCE = clsmembers