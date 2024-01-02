import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from config import OWNER_ID
import re

conn = sqlite3.connect("data/twit_tables.db")
cur = conn.cursor()

VERBOSE = False

class TwitCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    # ------------------------------------------------
    
    @commands.Cog.listener('on_message')
    async def twitter_url_fix(self, message):
        if opted_in_check(message.guild.id, message.author.id):
            if re.match("(https?:\/\/)(?:www.)?(?:x|twitter|tiktok)(.com.*)", message.content):
                replaced = re.sub("(https?:\/\/)(?:www.)?(?:x|twitter)(.com.*)", "\g<1>fxtwitter\g<2>", message.content)
                replaced = re.sub("(https?:\/\/)(?:www.)?tiktok(.com.*)", "\g<1>vxtiktok\g<2>", replaced)
                print(replaced)
                await message.channel.send(replaced)
                await message.delete()
    
    async def opted_in_ac(self, 
                        interaction: discord.Interaction, 
                        current: str
                        ) -> list[app_commands.Choice[str]]:
        options = [r for r in interaction.guild.members]
        choices = [r.display_name for r in options if current.lower() in r.name.lower() or current.lower() in r.display_name.lower()][:25]
        return [app_commands.Choice(name=choice, value=choice) for choice in choices]

    @app_commands.command(description='Have your x.com links replaced with fxtwitter.com')
    @app_commands.autocomplete(user = opted_in_ac)
    async def twit_fix(self, interaction, user:str):
        member = [m for m in interaction.guild.members if 
                    m.name == user or m.display_name == user]
        if member:
            opted = sql_fetch('user', 'opted', interaction.guild.id)
            member = member[0]
            print(member.id, opted)
            if member.id not in opted:
                cur.execute(f"""INSERT OR IGNORE INTO opted VALUES
                                ({interaction.guild.id},{member.id})""")
                conn.commit()
                    
                await interaction.response.send_message(
                    f"User {member.display_name} will have their twit links fixed.", ephemeral=True)
            else:
                cur.execute(f"""DELETE FROM opted WHERE
                            guild = {interaction.guild.id} AND user={member.id}""")
                conn.commit()
                await interaction.response.send_message(
                    f"User {member.display_name} will no longer have twit links fixed.", ephemeral=True)
        else:
            await interaction.response.send_message(
                f"I don't know who {user} is? ", ephemeral=True)

# ----------------------------------------------------

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(TwitCog(bot))

# Support Discord Functions

def sql_fetch(col, table, guild):
    query = f"""
            SELECT DISTINCT 
                {col} 
            FROM {table}
            WHERE 
                guild = {guild}
            """
    return [ x[0] for x in cur.execute(query).fetchall() ]

def opted_in_check(guild_id, id):
    result = sql_fetch('user', 'opted', guild_id)
    if id in result: return True
    else: return False

# Non Discord Functions

