import discord
from discord.ext import commands
from discord import app_commands
from random import sample
import re
import sqlite3
import re

VERBOSE = False
conn = sqlite3.connect("data/trainer_rewards.db")
cur = conn.cursor()

class TrainerCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    async def trainer_class_autocomplete(self, 
                                          interaction: discord.Interaction, 
                                          current: str
                                          ) -> list[app_commands.Choice[str]]:
        query = "SELECT DISTINCT name FROM class"
        options = [ x[0] for x in cur.execute(query).fetchall() ]
        choices = [c for c in options if current.lower() in c.lower()][:25]
        return [app_commands.Choice(name=choice, value=choice) for choice in choices]
    
    async def trainer_rank_autocomplete(self, 
                                          interaction: discord.Interaction, 
                                          current: str
                                          ) -> list[app_commands.Choice[str]]:
        if len(current) < -1:
            return []
        else:
            query = f""" SELECT DISTINCT name FROM rank"""
            options = [x[0]  for x in cur.execute(query).fetchall()]
            choices = [c for c in options if current.lower() in c.lower()][:25]
            return [app_commands.Choice(name=choice, value=choice) for choice in choices]
    
    @app_commands.command(description="Get Poke Awarded After a Battle")
    @app_commands.autocomplete(tclass = trainer_class_autocomplete)
    @app_commands.autocomplete(trank = trainer_rank_autocomplete)
    async def trainer_battle_rewards(self, interaction, tclass:str, trank:str):
        try:
            cash = cur.execute(f"SELECT DISTINCT cash FROM class WHERE name='{tclass}'").fetchall()[0][0]
            multi = cur.execute(f"SELECT DISTINCT multiplier FROM rank WHERE name='{trank}'").fetchall()[0][0]
            await interaction.response.send_message(f"After your fight with a *{trank} {tclass}*,\n You got ***{cash*multi}*** *({cash}+{multi})* for winning!")
        except Exception as e:
            await interaction.response.send_message(
                f"There was a problem... I had an {e.args[0]}")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(TrainerCog(bot))


# Non Discord Functions

if __name__ == "__main__":
    cash = cur.execute(f"SELECT DISTINCT cash FROM class WHERE name='Aroma Lady'").fetchall()[0][0]
    multi = cur.execute(f"SELECT DISTINCT multiplier FROM rank WHERE name='Ace'").fetchall()[0][0]