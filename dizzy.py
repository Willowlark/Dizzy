import discord
import asyncio
import re
import random
import json
from copy import deepcopy

from sys import maxsize
from datetime import datetime
from datetime import timedelta
from os.path import join
from os import makedirs
from collections import Mapping
from diary import Diary
from auth import *
import commander

# TODO: Review loading and saving from Cloudant
# TODO: IO variable logic
# TODO: Commands from json?

diary = Diary(CLOUDANT_USER, CLOUDANT_PASS)
diary.select_db('dizzy')

LEWDS = []
BANS = []
COUNTERS = {}

client = discord.Client()
parser = commander.Commander(client, ['!', '<:spiral:392726979197140992>', 'Dizzy,'])

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    entrance = "Hello! I made it a'okay!" if random.randint(1,10) != 1 else "*Trips on the doorframe* Auu~" 
    # await client.send_message(get_channel_by_name('general'), entrance)

@client.event
async def on_message(message):
    
    io = parser.getio(message)
    
    if io in [1, 3]:
        load_state()
        build_commands()

    await parser.execute(message)
    
    if io in [2, 3]:
        save_state()
        load_state()
        build_commands()
    
    path = join('logs', message.channel.name)
    makedirs(path, exist_ok=1)
    with open(join(path,message.timestamp.date().isoformat()+'.txt'), 'a') as f:
        try:
            name = message.author.nick 
        except:
            name = message.author.name
        f.write(name + ": " + message.content + '\n')
        print(name + ": " + message.content)


async def time_trigger():
    await client.wait_until_ready()
    while not client.is_closed:
        now = datetime.now()
        if now.weekday() in [0,3]:
            if now.hour == 11:
                await client.send_message(get_channel_by_name("general"), "GM posts come out today.")
                await asyncio.sleep(3600)
        await asyncio.sleep(60)

# Find a channel object via the name of the channel.
def get_channel_by_name(string):
    for channel in client.get_all_channels():
        if channel.name == string:
            return channel

def load_state():
    global LEWDS
    global BANS
    global COUNTERS
    optionals = diary.load_document('sets')
    LEWDS.clear()
    BANS.clear()
    LEWDS.extend(optionals['lewds'])
    BANS.extend(optionals['ban_reasons'])

    COUNTERS = diary.load_document("counters")

    print('Loaded data from Diary.')

def save_state():
    global COUNTERS
    # remote = diary.load_document('counters')
    # remote = COUNTERS
    COUNTERS.save()

def build_commands():
    parser.commands.clear()
    parser.add(commander.RandomReply(triggers=['\U0001F51E'], options=['https://i.imgur.com/JbVqZOn.jpg'], pattern='(lewd)'))
    parser.add(commander.RandomReply(options=LEWDS, pattern='(lewd)', io=1))
    parser.add(commander.RandomReply(options=BANS, pattern='(kick|ban|kickban)', io=1))
    parser.add(commander.Timecheck(pattern='(timecheck)'))
    parser.add(commander.Choose(pattern='(choose) (.*)'))
    parser.add(commander.Stab(pattern='(stab)'))
    parser.add(commander.Refresh(pattern='(refresh)', io=1))

    log = commander.Log(pattern='(log) ([^ ]*)')
    log.requireauthor('Willowlark')
    parser.add(log)

    postday = commander.Reply(options='Yes, it is "Post Day".', triggers=[''], pattern='.*post day.*yet.*')
    postday.setfunc(lambda: datetime.now().weekday() in [0, 3])
    parser.add(postday)
    
    notpostday = commander.Reply(options="No, it isn't post day.", triggers=[''], pattern='.*post day.*yet.*')
    notpostday.setfunc(lambda: datetime.now().weekday() not in [0, 3])
    parser.add(notpostday)
    
    parser.add(commander.Reply(options='https://i.imgur.com/55sx3FG.png', pattern='(tsun)'))
    parser.add(commander.Reply(options='https://i.imgur.com/hXuK1cP.png', pattern='(hush)'))
    parser.add(commander.Reply(options='https://i.imgur.com/gilOf0I.gif', pattern='(teamwork)'))
    parser.add(commander.Reply(options='https://i.imgur.com/no93Chq.png', pattern='(prick)'))
    parser.add(commander.Reply(options='I ship Knight Light!', triggers=[''], pattern='.*ship.*knight light.*|.*knight light.*ship.*'))

    parser.add(commander.CounterIncrement(options=COUNTERS, pattern='(counter) ([^ ]+) (add|sub) ([0-9]+)', io=3))
    parser.add(commander.CounterCheck(options=COUNTERS, pattern='(counter) ([^ ]+) (check)', io=3))
    parser.add(commander.CounterList(options=COUNTERS, pattern='(counter) (list)', io=1))
    setcounter = commander.CounterSet(options=COUNTERS, pattern='(counter) ([^ ]+) (set) ([0-9]+)', io=3)
    setcounter.requireauthor('Willowlark')
    parser.add(setcounter)

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
build_commands()
client.loop.create_task(time_trigger())
client.run(TOKEN)