import discord
from discord.ext import commands
import fire

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

MY_GUILD = discord.Object(id='992097929840050357') 
bot = commands.Bot(command_prefix='?', description='description', intents=intents)

cogs = [
    'cogs.dice_cog', 
    'cogs.rolltables_cog', 
    'cogs.apartment_cog'
    ]

@bot.event
async def on_ready():
    # if CLEAR:
    #     bot.tree.clear_commands(guild=None)
    #     bot.tree.clear_commands(guild=MY_GUILD)
    #     await bot.tree.sync(guild=MY_GUILD)
    #     await bot.tree.sync()
    #     exit()
    
    for cog in cogs:
       await bot.load_extension(cog)
    await bot.tree.sync()

    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.tree.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction, local:bool=False):
    if interaction.user.id == 184437198865563648:
        if local: 
            bot.tree.copy_global_to(guild=MY_GUILD)
            await bot.tree.sync(guild=MY_GUILD)
        else: 
            await bot.tree.sync()
        print('Command tree synced.')
    else:
        await interaction.response.send_message('You must be the owner to use this command!')

@bot.tree.command(name='reload')
async def reload(interaction: discord.Interaction):
    """Refresh"""
    if interaction.user.id == '184437198865563648':
        for mycog in cogs:
            await bot.reload_extension(mycog)
            
        await interaction.response.send_message('Reloaded')

def run():
    bot.run('MTEyMDE3MjcxNDgyMTQyNzIyMg.G3VhQe.d1PVzQLRhCR5G1Jbo-hFTRUCh7XCfKH363wZJ8')
  
if __name__ == '__main__':
  fire.Fire(run)
