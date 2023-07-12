import discord
from discord.ext import commands
from cogs.dice_cog import DiceCog
from cogs.apartments import ApartmentCog

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description='description', intents=intents)

@bot.event
async def on_ready():
    await bot.add_cog(ApartmentCog(bot))
    await bot.add_cog(DiceCog(bot))
    await bot.tree.sync()
    
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.hybrid_command()
async def refresh(ctx):
    """Refresh"""
    await bot.tree.sync()
    await ctx.send('Refreshed')

# @client.tree.command()
# async def roll(interaction: discord.Interaction, *, dice:str):
#     og, rolls, total = DiceCog.parse(dice)
#     await interaction.response.send_message(f"Rolled `{og}` and got {total}!\nThe rolls were :*{rolls}*")

bot.run('MTEyMDE3MjcxNDgyMTQyNzIyMg.G3VhQe.d1PVzQLRhCR5G1Jbo-hFTRUCh7XCfKH363wZJ8')