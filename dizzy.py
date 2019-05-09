import discord
import asyncio
import random
import json
import argparse

from datetime import datetime
from os.path import join
from os import chdir, listdir, makedirs

import server 
from auth import TOKEN

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--disablelogs', action='store_false',
                    help='disable logging')


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
    # await get_channel_by_name('general', "The Realm of Aurii").send(entrance)

@client.event
async def on_message(message):
    
    source_server = message.guild.name
    
    if source_server in servers:
        await servers[source_server].handle(message, logging=args.disablelogs)
    else:
        print("server {} not handled right now.".format(source_server))

@client.event
async def on_member_update(before, after):
    
    source_server = after.guild
    if source_server.name in servers:
        await servers[source_server.name].on_member_update(before, after, source_server)
    else:
        print("server {} not handled right now.".format(source_server.name))

# Find a channel object via the name of the channel.
def get_channel_by_name(string, server=None):
    for channel in client.get_all_channels():
        if channel.name == string and (server == channel.guild.name or server is None):
            return channel

if __name__ == '__main__':
    args = parser.parse_args()
    # client.loop.create_task(time_trigger()) #CRIT How to add a custom task.
    client.run(TOKEN)