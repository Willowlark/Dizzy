import re
import random
import asyncio
import pastebin

from datetime import datetime
from datetime import timedelta
from sys import maxsize
from os.path import join

# TODO: Help input as a constructor value, which is placed in __str__.
# TODO: Help interator for the Commander object
# TODO: User stats (each user gets a document)
# TODO: Dice bot

class Commander(object):

    def __init__(self, client, triggers):
        self.client = client
        self.triggers = triggers
        self.commands = []

    async def execute(self, message):
        for command in self.commands:
            await command.execute(message)
        
    def match(self, message):
        for command in self.commands:
            x = command.match(message)
            if x:
                return x

    def getio(self, message):
        for command in self.commands:
            x = command.match(message)
            if x:
                return command.getio()
        return 0

    def add(self, cmd): 
        if not cmd.client:
            cmd.client = self.client
        if not cmd.triggers:
            cmd.triggers = self.triggers
            cmd.compile()
        self.commands.append(cmd)

class Command(object):

    def __init__(self, client=None, triggers=None, options=[], pattern='', io=0, info=None):
        self.client = client
        self.triggers = triggers
        self.options = options
        self.pattern = pattern
        self.io = io
        self.info = info if info else "A command using pattern: "+self.pattern

        self.compile()

        self.author = []
        self.notauthor = []
        self.func = None

    def compile(self):
        triggers = [''] if not self.triggers else self.triggers
        self.trigger_match = '^({t}){c}|^({t}) {c}'.format(t='|'.join(triggers), c='{c}')
        self.expression = re.compile(self.trigger_match.format(c=self.pattern), flags=re.DOTALL)
    
    def match(self, message):
        match = self.expression.match(message.content)
        if match:
            return [x for x in match.groups() if x is not None]
        else:
            return []

    def getio(self):
        return self.io

    async def execute(self, message):
        match = self.match(message)
        if match: 
            if self.check(message):
                await self.action(message, match)
            else:
                await self.client.send_message(message.channel, "I'm not allowed to let you do that, {}.".format(message.author.name))

    async def action(self, message, match):
        await asyncio.sleep(10)
        await self.client.send_message(message.channel, 'Waited!')

    def check(self, message):
        
        # Author must/not
        if self.author:
            if message.author.name not in self.author:
                return False
        if self.notauthor:
            if message.author.name in self.notauthor:
                return False

        # Lambda 
        if self.func:
            if not self.func(): 
                return False
        
        return True

    def banauthor(self, name):
        self.notauthor.append(name)
    
    def requireauthor(self, name):
        self.author.append(name)

    def setfunc(self, func):
        self.func = func

class ForkCommand(Command):
    pass

class RandomReply(Command):

    async def action(self, message, match):
        link = random.choice(self.options)
        await self.client.send_message(message.channel, link)

class Reply(Command):

    async def action(self, message, match):
        await self.client.send_message(message.channel, self.options)

class Timecheck(Command):

    async def action(self, message, match):
        now = datetime.utcnow()
        nowam = now - timedelta(hours=4)
        nowjp = now + timedelta(hours=9)
        msg = "It's currently {} in EST and {} in Weebland.".format(
            nowam.strftime("%H:%M"), nowjp.strftime("%H:%M"))
        await self.client.send_message(message.channel, msg)

class Choose(Command):

    async def action(self, message, match):
        options = match[2].split(',')
        option = random.choice(options) if "knight light" not in options else "knight light"
        await self.client.send_message(message.channel, 'You should choose '+ option)

class Log(Command):

    async def action(self, message, match):
        channel = match[2]
        queue = []
        attrition = None
        auth = None
        tmp = await self.client.send_message(message.channel, 'Pulling messages from ' + channel+':')
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
        open(join('batch-logs', channel+'.md'), 'w').writelines(reversed(queue))
        url = pastebin.paste(channel, '\n'.join(reversed(queue)))
        await self.client.send_message(message.channel, 'Logging done @ ' + repr(url))

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
        who = random.choice([x for x in list(message.server.members) if x.name != "Dizzy"])
        who = who.nick if who.nick else who.name
            
        # who = who.mention
        what = random.choice(['shanks', 'stabs'])
        
        act = '*{} {}!*'.format(what, who) if random.randint(1,10) != 1 else '*attempts to {} {}; but trips and stabs herself instead*!'.format(what, who)
        
        if message.author.name == "Halim": # Create the fork command for this.
            await self.client.send_message(message.channel, "Stop making me do this...")
        else:        
            await self.client.send_message(message.channel, act)

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
        #     await client.send_message(message.channel, '{} has {} in the {} stat.'.format(user, leaf['value'], keyring[-1]))
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
        #                 await client.send_message(message.channel, "Sorry, you can't access that stat.")
        #         else:
        #             leaf['locked'] = 0 if leaf['locked'] else 1
        #             save_state()
        #             await client.send_message(message.channel, 'The {} stat is in state {}.'.format(keyring[-1], leaf['value']))
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
        #                 await client.send_message(message.channel, "Sorry, you can't modify that stat.")
        #         else:
        #             leaf['value']+= amnt
        #             user = keyring[0] if len(keyring)>1 else "The server"
        #             await client.send_message(message.channel, '{} has {} in the {} stat.'.format(user, leaf['value'], keyring[-1]))
        #             save_state()
        #     else:
        #         print('No stat found for', options)

class CounterIncrement(Command):

    async def action(self, message, match):
        target, op, amnt = match[2:]
        amnt = int(amnt)
        COUNTERS = self.options

        if target not in COUNTERS:
            await self.client.send_message(message.channel, "I'm not counting those right now.")
        else:
            value = COUNTERS[target]
            if op == "add":
                COUNTERS[target]+=amnt
                await self.client.send_message(message.channel, "The {} count is now {}!".format(target, COUNTERS[target]))
            elif op == "sub":
                COUNTERS[target]-=amnt
                await self.client.send_message(message.channel, "The {} count is now {}!".format(target, COUNTERS[target]))
            else:
                await self.client.send_message(message.channel, "I don't know how to do that, sorry.")

class CounterCheck(Command):
    
    async def action(self, message, match):
        target, op = match[2:]
        COUNTERS = self.options

        if target not in COUNTERS:
            await self.client.send_message(message.channel, "I'm not counting those right now.")
        else:
            await self.client.send_message(message.channel, "The {} count {}.".format(target, COUNTERS[target]))

class CounterSet(Command):

    async def action(self, message, match):
        target, op, amnt = match[2:]
        amnt = int(amnt)
        COUNTERS = self.options

        COUNTERS[target] = amnt
        
        await self.client.send_message(message.channel, "The {} count is now {}!".format(target, COUNTERS[target]))

class CounterList(Command):

    async def action(self, message, match):
        
        COUNTERS = self.options

        lines = ["Here's what I have.\n", '```']
        for key, value in COUNTERS.items():
            if key[0] != '_':
                lines.append("{} count is at {}.\n".format(key, value))
        lines.append('```')

        await self.client.send_message(message.channel, "".join(lines))

class Refresh(Command):

    async def action(self, message, match):
        await self.client.send_message(message.channel, "I'll go reread my notes!")

class Ghost(Command):

    async def action(self, message, match):
        content = match[2]
        await self.client.delete_message(message)
        await self.client.send_message(message.channel, content)
        # for m in content.split('\n'):
            # await self.client.send_message(message.channel, m)