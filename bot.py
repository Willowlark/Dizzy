import discord
from discord.ext import commands
import fire
from config import BOT_TOKEN

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

MY_GUILD = discord.Object(id='992097929840050357') 
bot = commands.Bot(command_prefix='?', description='description', intents=intents)

cogs = [
    'cogs.dice_cog', 
    'cogs.rolltables_cog',
    'cogs.role_cog',
    'cogs.twit_cog',
    'cogs.trainer_cog'
    ]

@bot.event
async def on_ready():
    for cog in cogs:
       await bot.load_extension(cog)
    await bot.tree.sync()

    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.tree.command(name='pokerolefaq', description='Share the Pokerole FAQ')
async def pokerolefaq(interaction: discord.Interaction):
    await interaction.response.send_message('Check the FAQ here: https://wiki.aurii.us/doku.php?id=pokerole-server:server_faq ')
   

@bot.tree.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction, local:bool=False):
    if interaction.user.id == 184437198865563648:
        if local: 
            bot.tree.copy_global_to(guild=MY_GUILD)
            await bot.tree.sync(guild=MY_GUILD)
            print('Guild Command tree synced.')
        else: 
            await bot.tree.sync()
        print('Command tree synced.')
    else:
        await interaction.response.send_message('You must be the owner to use this command!')

@bot.tree.command(name='clear', description='Owner only')
async def clear(interaction: discord.Interaction, local:bool=False):
    if interaction.user.id == 184437198865563648:
        if local: 
            bot.tree.clear_commands(guild=MY_GUILD)
            await bot.tree.sync(guild=MY_GUILD)
            print('Guild Command tree cleared.')
        else: 
            bot.tree.clear_commands(guild=None)
            await bot.tree.sync()
        print('Command tree cleared.')
    else:
        await interaction.response.send_message('You must be the owner to use this command!')

@bot.tree.command(name='reload')
async def reload(interaction: discord.Interaction):
    """Refresh"""
    if interaction.user.id == '184437198865563648':
        for mycog in cogs:
            await bot.reload_extension(mycog)
            
        await interaction.response.send_message('Reloaded')
    else:
        await interaction.response.send_message('You must be the owner to use this command!')

# @bot.listen('on_message')
# async def twitter_url_fix(message):
#     if re.match("(https?:\/\/)x(.com.*)", message.content):
#         replaced = re.sub("(https?:\/\/)x(.com.*)", "\g<1>fxtwitter\g<2>", message.content)
#         print(replaced)
#         await message.channel.send(replaced)
#         await message.delete()

def run():
    bot.run(BOT_TOKEN)
  
if __name__ == '__main__':
  fire.Fire(run)
