import discord
import asyncio
import re
import random
import json
from copy import deepcopy

from sys import maxsize
from os.path import join
from datetime import datetime
from datetime import timedelta
from collections import Mapping

TRIGGERS = ['!', '<:spiral:392726979197140992>', 'Dizzy,', '\U0001F51E']
# Matches either the first word of a string, returning the trigger and whatever followed the trigger, 
# or the first word which is entirely a trigger and the immediately following word.
TRIGGER_MATCH = re.compile('^({t})(\w+)|^({t}) (\w+)'.format(t='|'.join(TRIGGERS)))
TOKEN = 'MzkyNjk1MDg5NTQ3NDQ0MjU2.DRq9Ug.NSGrtWvwAk3fONQ6mACtRNoZP7Q'
STATE = {}
LEWDS = open('lewd_links').readlines()
BANS = open('ban_responses').readlines()
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    entrance = "Hello! I made it a'okay!" if random.randint(1,10) != 1 else "*Trips on the doorframe* Auu~" 
    await client.send_message(get_channel_by_name('general'), entrance)

@client.event
async def on_message(message):
    trigger, cmd = get_cmd(message.content)
    
    # Special triggers
    if trigger == '\U0001F51E':
        # Special lewd for Marisa meme
        if cmd == 'lewd':
            link = 'https://i.imgur.com/JbVqZOn.jpg'
            await client.send_message(message.channel, link)
    
    elif trigger:
        # Messages in last 20,000. 
        if cmd == 'sent':
            counter = 0
            tmp = await client.send_message(message.channel, 'Calculating messages...')
            async for log in client.logs_from(message.channel, limit=20000):
                if log.author == message.author:
                    counter += 1
            await client.edit_message(tmp, 'You have sent {} messages.'.format(counter))
        
        # Tsundere mode
        if cmd == 'tsun':
            link = 'https://i.imgur.com/55sx3FG.png'
            await client.send_message(message.channel, link)
        
        # Hush
        if cmd == 'hush':
            link = 'https://i.imgur.com/hXuK1cP.png'
            await client.send_message(message.channel, link)
        
        # teamwork
        if cmd == 'teamwork':
            link = 'https://i.imgur.com/gilOf0I.gif'
            await client.send_message(message.channel, link)
        
        # Prick
        if cmd == 'prick':
            link = 'https://i.imgur.com/no93Chq.png'
            await client.send_message(message.channel, link)
        
        # Lewd commands
        elif cmd == 'lewd':
            link = random.choice(LEWDS)
            await client.send_message(message.channel, link)
        
        # Logging commands
        elif cmd == 'log' and message.author.name == "Willowlark":
            channel = re.search('log ([^ ]*)', message.content).group(1)
            queue = []
            tmp = await client.send_message(message.channel, 'Pulling messages from...')
            async for log in client.logs_from(get_channel_by_name(channel),limit=maxsize):
                queue.append(logged_format(log))
            open(join('logs', channel+'.md'), 'w').writelines(reversed(queue))
            await client.send_message(message.channel, 'Logging done.')

        # Choose between comma separated values
        elif cmd == 'choose':
            options = re.search('choose (.*)', message.content).group(1).split(',')
            option = random.choice(options) if "knight light" not in options else "knight light"
            await client.send_message(message.channel, 'You should choose '+ option)
        
        # Stab someone randomly
        elif cmd == 'stab':
            who = random.choice([x for x in list(message.server.members) if x.name != "Dizzy"])
            who = who.nick if who.nick else who.name
                
            # who = who.mention
            what = random.choice(['shanks', 'stabs'])
            
            act = '*{} {}!*'.format(what, who) if random.randint(1,10) != 1 else '*attempts to {} {}; but trips and stabs herself instead*!'.format(what, who)
            
            if message.author.name == "Halim":
                await client.send_message(message.channel, "Stop making me do this...")
            else:        
                await client.send_message(message.channel, act)

        elif cmd == 'gift':
            gift = re.search('gift (.*)', message.content).group(1)
            if gift == 'caramel':
                await client.send_message(message.channel, "I love caramel, thank you! ❤️")
            else:
                await client.send_message(message.channel, "Thank you!")
    
        elif cmd == 'stats':
            options = re.search('stats (.*)', message.content).group(1).split(',')
            try: 
                options.append(message.author.nick)
            except:
                pass
            options.append(message.author.name)
            options = [x.strip() for x in options]
            keyring, leaf = _stat_search(STATE['stats'], options, deep=0)
            
            if leaf is not None:
                user = keyring[0] if len(keyring)>1 else "The server"
                await client.send_message(message.channel, '{} has {} in the {} stat.'.format(user, leaf['value'], keyring[-1]))
            else:
                print('No stat found for', options)
                
        elif cmd == 'lock':
            options = re.search('lock (.*)', message.content).group(1).split(',')
            try: 
                options.append(message.author.nick)
            except:
                pass
            options.append(message.author.name)
            options = [x.strip() for x in options]
            keyring, leaf = _stat_search(STATE['stats'], options, deep=0)
            
            if leaf is not None:
                if leaf['locked'] and len(keyring)>1:
                    if message.author.name not in keyring and message.author.name != "Willowlark":
                        await client.send_message(message.channel, "Sorry, you can't access that stat.")
                else:
                    leaf['locked'] = 0 if leaf['locked'] else 1
                    save_state()
                    await client.send_message(message.channel, 'The {} stat is in state {}.'.format(keyring[-1], leaf['value']))
            else:
                print('No stat found for', options)
                
        elif cmd == 'level':
            match = re.search('level ([^ ]+) (.*)', message.content)
            amnt = int(match.group(1))
            options = match.group(2).split(',')
            try: 
                options.append(message.author.nick)
            except:
                pass
            options.append(message.author.name)
            options = [x.strip() for x in options]
            keyring, leaf = _stat_search(STATE['stats'], options, deep=0)
            
            if leaf is not None:
                if leaf['locked'] and len(keyring)>1:
                    if message.author.name not in keyring and message.author.name != "Willowlark":
                        await client.send_message(message.channel, "Sorry, you can't modify that stat.")
                else:
                    leaf['value']+= amnt
                    user = keyring[0] if len(keyring)>1 else "The server"
                    await client.send_message(message.channel, '{} has {} in the {} stat.'.format(user, leaf['value'], keyring[-1]))
                    save_state()
            else:
                print('No stat found for', options)
        
        elif cmd in ['kickban', 'ban', 'kick']:
            link = random.choice(BANS)
            await client.send_message(message.channel, link)
    
    # Parse the text for patterns
    else:
        if re.search('.*post day.*yet.*', message.content):
            if datetime.now().weekday() in [0, 3]:
                await client.send_message(message.channel, 'Yes, it is "Post Day".')
            else:
                await client.send_message(message.channel, "No, it isn't post day.")
        if re.search('.*ship.*knight light.*|.*knight light.*ship.*', message.content):
                await client.send_message(message.channel, "I ship Knight Light!")
        

async def time_trigger():
    await client.wait_until_ready()
    while not client.is_closed:
        now = datetime.now()
        if now.weekday() in [0,3]:
            if now.hour == 11:
                await client.send_message(get_channel_by_name("general"), "GM posts come out today.")
        await asyncio.sleep(((now + timedelta(hours=1))-now).total_seconds())

# Returns the trigger used and the command sent via
def get_cmd(string):
    match = TRIGGER_MATCH.match(string)
    if match:
        match = match.groups()
        match = [x for x in match if x is not None]
        return match
    else:
        return [None, None]

# Find a channel object via the name of the channel.
def get_channel_by_name(string):
    for channel in client.get_all_channels():
        if channel.name == string:
            return channel

# Return a formatted string to add to a log.
def logged_format(log):
    try:
        name = log.author.nick 
    except:
        name = log.author.name
    return "**"+name + ':**\n\n' + log.content + '\n\n'

def load_state():
    global STATE
    STATE = json.loads(open('state.json').read())

def save_state():
    open('state.json', 'w').write(json.dumps(STATE))

def savenow(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        save_state()
    return wrapper

def _stat_search(depth, keys, deep=1):
    for key in keys:
        if key in depth:
            if 'value' in depth[key]:
                depth[key]['value']= depth[key]['value']
                return [key], depth[key] # it's a leaf
            else:
                keyring, leaf = _stat_search(depth[key], keys)
                keyring.insert(0, key)
                return keyring, leaf
    # no matches at this depth.
    if deep:
        nodes = [k for k,v in depth.items() if 'value' not in depth[k]]
        for node in nodes:
            keyring, leaf = _stat_search(depth[node], keys)
            if leaf:
                keyring.insert(0, key)
                return keyring, leaf
    return [None], None # base case.

load_state()
client.loop.create_task(time_trigger())
client.run(TOKEN)