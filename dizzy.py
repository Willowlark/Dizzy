import discord
import asyncio
import random
import json
import argparse

from datetime import datetime
import arrow
from os.path import join
from os import chdir, listdir, makedirs

from auth import TOKEN
from bot import Engine

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--disablelogs', action='store_false',
                    help='disable logging')

client = discord.Client()
engine = Engine()

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
    await engine.on_message(message)
    
# @client.event
# async def on_member_update(before, after):
    
#     source_server = after.guild
#     if source_server.name in servers:
#         await servers[source_server.name].on_member_update(before, after, source_server)
#     # else:
#     #     print("server {} not handled right now.".format(source_server.name))

# @client.event
# async def on_message_delete(message):
    
#     source_server = message.guild
#     if source_server.name in servers:
#         await servers[source_server.name].on_message_delete(message)
#     # else:
#     #     print("server {} not handled right now.".format(source_server.name))

# Find a channel object via the name of the channel.
def get_channel_by_name(string, server=None):
    for channel in client.get_all_channels():
        if channel.name == string and (server == channel.guild.name or server is None):
            return channel

async def minute_ticker():
    ldt = arrow.now()
    ldt = ldt.to('America/New_York')
    while 1:
        now = arrow.now()
        nowam = now.to('America/New_York')
        if now.minute != ldt.minute:
            ldt = now
            for server in servers:
                await servers[server].ticker(nowam)
        # print(f"{now.hour}:{now.minute}:{now.second} - {ldt.hour}:{ldt.minute}:{ldt.second}")
        await asyncio.sleep(1)

if __name__ == '__main__':
    args = parser.parse_args()
    client.run(TOKEN)
