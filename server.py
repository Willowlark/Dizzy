import json
from datetime import datetime

from skills import commands
from skills.parser import Parser
import diary
import logger
from discord import Status

class Interface(object):
    
    def __init__(self, client, config):
        self.client = client
        self.config = config
        
        self.name = config['Server Name']
        
        self.diaries = {}
        for db in self.config["DBs"]:
            x = diary.publisher(db)
            self.diaries[x.db_name] = x
        
        self.loggers = []
        for log in config['Loggers']:
            self.loggers.append(logger.create(log))
        
        self.command_set = self.generate_commands()
        
    def generate_commands(self):
        return None
        
    async def handle(self, message, logging=True):
        
        await self.command_set.execute(message)
        if  logging:
            for log in self.loggers:
                log.log(message)
    
    async def on_member_update(self, before, after, guild):
        pass
    
    async def on_message_delete(self, message):
        pass

class Aurii(Interface):
    
    async def on_member_update(self, before, after, guild):
        CHANNELS = self.diaries['Local'].data['RFA']['Channels']
        newstatus = str(after.status)
        oldstatus = str(before.status)
        
        for channel, rfa in CHANNELS.items():
            
            if after.name in rfa['Members']:
                for channel in guild.text_channels:
                    if rfa['Name'] == channel.name and rfa['Enabled'] == 'true': # channel is the targeted channel
                        
                        user = after.nick if after.nick is not None else after.name
                        if newstatus == 'online' and oldstatus == 'offline':
                            await channel.send(f'*{user} has entered the chatroom*')
                        elif newstatus == 'offline':
                            await channel.send(f'*{user} has left the chatroom*')
                        else:
                            pass
                        
                        online = []
                        for user in rfa['Members']:
                            for member in guild.members:
                                if member.name == user and str(member.status) == 'online':
                                    online.append(member.nick if member.nick is not None else member.name)
                        await channel.edit(topic=', '.join(online))

    async def on_message_delete(self,message):
        my_id = 184437198865563648
        
        me = self.client.get_user(my_id)
        await me.send(f"{message.author.name} deleted\n\n>>> {message.content}")

    def generate_commands(self):
        command_set = Parser(['!', 'Dizzy,'])
        
        command_set.add(commands.RandomReply(triggers=['\U0001F51E'], options=['https://i.imgur.com/JbVqZOn.jpg'], pattern='(lewd)'))
        command_set.add(commands.RandomReply(options=self.diaries['Local'].data["Sets"]['lewds'], pattern='(lewd)'))
        command_set.add(commands.RandomReply(options=self.diaries['Local'].data["Sets"]['dabs'], pattern='(dab)'))
        command_set.add(commands.RandomReply(options=self.diaries['Local'].data["Sets"]['ban_reasons'], pattern='(kick|ban|kickban)'))
        command_set.add(commands.Timecheck(pattern='(timecheck)'))
        command_set.add(commands.Choose(pattern='(choose) (.*)'))
        command_set.add(commands.Stab(pattern='(stab)'))
        command_set.add(commands.Refresh(pattern='(refresh)', options=[self.diaries]))

        log = commands.Log(pattern='(log) ([^ ]*)')
        log.requireauthor('Willowlark')
        command_set.add(log)

        postday = commands.Reply(options='Yes, it is "Post Day".', triggers=[''], pattern='.*post day.*yet.*')
        postday.setfunc(lambda x: datetime.now().weekday() in [0, 3])
        command_set.add(postday)
        
        notpostday = commands.Reply(options="No, it isn't post day.", triggers=[''], pattern='.*post day.*yet.*')
        notpostday.setfunc(lambda x: datetime.now().weekday() not in [0, 3])
        command_set.add(notpostday)
        
        command_set.add(commands.Reply(options='https://i.imgur.com/55sx3FG.png', pattern='(tsun)'))
        command_set.add(commands.Reply(options='https://i.imgur.com/hXuK1cP.png', pattern='(hush)'))
        command_set.add(commands.Reply(options='https://i.imgur.com/gilOf0I.gif', pattern='(teamwork)'))
        command_set.add(commands.Reply(options='https://i.imgur.com/no93Chq.png', pattern='(prick)'))
        command_set.add(commands.Reply(options='https://i.imgur.com/JxOe5TA.jpg', pattern='(angryjess)'))
        command_set.add(commands.Reply(options='I ship Knight Light!', triggers=[''], pattern='.*ship.*knight light.*|.*knight light.*ship.*'))

        ghost = commands.Ghost(pattern='(ghost) (.*)')
        ghost.requireauthor('Willowlark')
        command_set.add(ghost)
        
        command_set.add(commands.Fudge(pattern='(fudge) ([+-]?[0-9]+)'))
        command_set.add(commands.Fudge(pattern='(fudge)'))

        command_set.add(commands.Headpat(options=self.diaries['Local'], pattern='(headpat)(.*)'))
        command_set.add(commands.IrlRuby(options=self.diaries['Local'], pattern='(irlRuby)(.*)'))
        
        x = commands.RFAMode(options=self.diaries['Local'], pattern='(rfamode) ([^ ]*) ([Tt]rue|[Ff]alse)')
        command_set.add(x)
        command_set.add(commands.RFAMembership(options=self.diaries['Local'], pattern='(rfamembership) ([^ ]+) ([^ ]+)'))



        x = commands.CounterIncrement(options=self.diaries['Local'], pattern='(counter) (add|sub) ([^ ]+) ([0-9]+)')
        command_set.add(x)
        
        x = commands.CounterCheck(options=self.diaries['Local'], pattern='(counter) (check) ([^ ]+)')
        command_set.add(x)
        
        x = commands.CounterRemove(options=self.diaries['Local'], pattern='(counter) (remove) ([^ ]+)')
        command_set.add(x)
        
        x = commands.CounterList(options=self.diaries['Local'], pattern='(counter) (list)')
        command_set.add(x)
        
        setcounter = commands.CounterSet(options=self.diaries['Local'], pattern='(counter) (set) ([^ ]+) ([0-9]+)')
        # setcounter.requireauthor('Willowlark')
        command_set.add(setcounter)



        # command_set.add(commands.CharactersScan(pattern='(chscan)', options=self.diaries['Local']))
        command_set.add(commands.CharacterLoad(pattern='(chload) ([^ ]*) (.*)', options=self.diaries['Local']))
        command_set.add(commands.CharacterCheck(pattern='(chcheck) ([^ ]*) (.*)', options=self.diaries['Local']))
        command_set.add(commands.CharacterList(pattern='(chlist)', options=self.diaries['Local']))
        command_set.add(commands.CharacterRoll(pattern='(chroll) ([^ ]*) ([^ ]*)', options=self.diaries['Local']))
        command_set.add(commands.CharacterMod(pattern='(chmod) ([^ ]*) ([^ ]*|Fate Points) ([0-9])', options=self.diaries['Local'])) # TODO Actual regex that takes split words.
        
        return command_set

class BNE(Interface):

    def generate_commands(self):
        command_set = Parser(['!', 'Dizzy,'])
        
        command_set.add(commands.RandomReply(triggers=['\U0001F51E'], options=['https://i.imgur.com/JbVqZOn.jpg'], pattern='(lewd)'))
        command_set.add(commands.RandomReply(options=self.diaries['Local'].data["Sets"]['lewds'], pattern='(lewd)'))
        command_set.add(commands.RandomReply(options=self.diaries['Local'].data["Sets"]['dabs'], pattern='(dab)'))
        command_set.add(commands.RandomReply(options=self.diaries['Local'].data["Sets"]['ban_reasons'], pattern='(kick|ban|kickban)'))
        command_set.add(commands.Choose(pattern='(choose) (.*)'))
        command_set.add(commands.Refresh(pattern='(refresh)', options=[self.diaries]))

        log = commands.Log(pattern='(log) ([^ ]*)')
        log.requireauthor('Willowlark')
        command_set.add(log)
        
        command_set.add(commands.Reply(options='https://i.imgur.com/55sx3FG.png', pattern='(tsun)'))
        command_set.add(commands.Reply(options='https://i.imgur.com/hXuK1cP.png', pattern='(hush)'))
        command_set.add(commands.Reply(options='https://i.imgur.com/gilOf0I.gif', pattern='(teamwork)'))
        command_set.add(commands.Reply(options='https://i.imgur.com/no93Chq.png', pattern='(prick)'))
        
        ghost = commands.Ghost(pattern='(ghost) (.*)')
        ghost.requireauthor('Willowlark')
        command_set.add(ghost)

        x = commands.CounterIncrement(options=self.diaries['Local'], pattern='(counter) (add|sub) ([^ ]+) ([0-9]+)')
        command_set.add(x)
        
        x = commands.CounterCheck(options=self.diaries['Local'], pattern='(counter) (check) ([^ ]+)')
        command_set.add(x)
        
        x = commands.CounterRemove(options=self.diaries['Local'], pattern='(counter) (remove) ([^ ]+)')
        command_set.add(x)
        
        x = commands.CounterList(options=self.diaries['Local'], pattern='(counter) (list)')
        command_set.add(x)
        
        setcounter = commands.CounterSet(options=self.diaries['Local'], pattern='(counter) (set) ([^ ]+) ([0-9]+)')
        setcounter.requireauthor('Willowlark')
        command_set.add(setcounter)
        
        return command_set

class ASPN(Interface):

    def generate_commands(self):
        command_set = Parser(['!', 'Dizzy,'])
        
        command_set.add(commands.RandomReply(options=self.diaries['Local'].data["Sets"]['lewds'], pattern='(lewd)'))
        command_set.add(commands.RandomReply(options=self.diaries['Local'].data["Sets"]['dabs'], pattern='(dab)'))
        command_set.add(commands.RandomReply(options=self.diaries['Local'].data["Sets"]['ban_reasons'], pattern='(kick|ban|kickban)'))
        command_set.add(commands.Choose(pattern='(choose) (.*)'))
        command_set.add(commands.Refresh(pattern='(refresh)', options=[self.diaries]))

        log = commands.Log(pattern='(log) ([^ ]*)')
        log.requireauthor('Willowlark')
        command_set.add(log)
        
        command_set.add(commands.Reply(options='https://i.imgur.com/55sx3FG.png', pattern='(tsun)'))
        command_set.add(commands.Reply(options='https://i.imgur.com/hXuK1cP.png', pattern='(hush)'))
        command_set.add(commands.Reply(options='https://i.imgur.com/gilOf0I.gif', pattern='(teamwork)'))
        command_set.add(commands.Reply(options='https://i.imgur.com/no93Chq.png', pattern='(prick)'))

        ghost = commands.Ghost(pattern='(ghost) (.*)')
        ghost.requireauthor('Willowlark')
        command_set.add(ghost)
        
        command_set.add(commands.Fudge(pattern='(fudge) ([+-]?[0-9]+)|(fudge)'))

        x = commands.CounterIncrement(options=self.diaries['Local'], pattern='(counter) (add|sub) ([^ ]+) ([0-9]+)')
        command_set.add(x)
        
        x = commands.CounterCheck(options=self.diaries['Local'], pattern='(counter) (check) ([^ ]+)')
        command_set.add(x)
        
        x = commands.CounterRemove(options=self.diaries['Local'], pattern='(counter) (remove) ([^ ]+)')
        command_set.add(x)
        
        x = commands.CounterList(options=self.diaries['Local'], pattern='(counter) (list)')
        command_set.add(x)
        
        setcounter = commands.CounterSet(options=self.diaries['Local'], pattern='(counter) (set) ([^ ]+) ([0-9]+)')
        # setcounter.requireauthor('Willowlark')
        command_set.add(setcounter)

        # command_set.add(commands.CharactersScan(pattern='(chscan)', options=self.diaries['Local']))
        command_set.add(commands.CharacterLoad(pattern='(chload) ([^ ]*) (.*)', options=self.diaries['Local']))
        command_set.add(commands.CharacterCheck(pattern='(chcheck) ([^ ]*) (.*)', options=self.diaries['Local']))
        command_set.add(commands.CharacterList(pattern='(chlist)', options=self.diaries['Local']))
        command_set.add(commands.CharacterRoll(pattern='(chroll) ([^ ]*) ([^ ]*)', options=self.diaries['Local']))
        command_set.add(commands.CharacterMod(pattern='(chmod) ([^ ]*) ([^ ]*|Fate Points) ([0-9])', options=self.diaries['Local'])) # TODO Actual regex that takes split words.
        
        return command_set

def create(client, config):
    parsed = json.loads(open(config).read())
    
    if parsed['Server Class'] == "Aurii":
        return Aurii(client, parsed)
    elif parsed['Server Class'] == 'BNE':
        return BNE(client, parsed)
    elif parsed['Server Class'] == 'ASPN':
        return ASPN(client, parsed)
    else:
        raise Exception("Server Class undefined.'")