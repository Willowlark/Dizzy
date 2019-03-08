import discord
import asyncio
import random
import json

from datetime import datetime
from os.path import join
from os import chdir, listdir, makedirs

import server 
from auth import TOKEN

client = discord.Client()
configs_path = 'configs'
chdir(configs_path)
configs = [f for f in listdir('.') if 'json' in f]

servers = {}
for config in configs:
    x = server.create(client, config)
    servers[x.name] = x

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    entrance = "Hello! I made it a'okay!" if random.randint(1,10) != 1 else "*Trips on the doorframe* Auu~" 
    # await client.send_message(get_channel_by_name('general', "The Realm of Aurii"), entrance)

@client.event
async def on_message(message):
    
    source_server = message.server.name
    
    try: 
        await servers[source_server].handle(message)
    except KeyError:
        print("server {} not handled right now, only logging.".format(source_server))
    
    # Logging
    path = join('logs', message.server.name, message.channel.name)
    makedirs(path, exist_ok=1)
    with open(join(path,message.timestamp.date().isoformat()+'.txt'), 'a') as f:
        try:
            name = message.author.nick
            assert name is not None
        except:
            name = message.author.name
        f.write(name + ": " + message.content + '\n')
        print(message.channel.name.upper() + ": " + name + ": " + message.content)


async def time_trigger():
    await client.wait_until_ready()
    while not client.is_closed:
        now = datetime.now()
        if now.weekday() in [0,3]:
            if now.hour == 11:
                # await client.send_message(get_channel_by_name("ooc"), "GM posts come out today.")
                await asyncio.sleep(3600)
        await asyncio.sleep(60)

# Find a channel object via the name of the channel.
def get_channel_by_name(string, server=None):
    for channel in client.get_all_channels():
        if channel.name == string and (server == channel.server.name or server is None):
            return channel

client.loop.create_task(time_trigger())
client.run(TOKEN)