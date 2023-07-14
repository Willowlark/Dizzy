import discord
from discord.ext import commands
from discord import app_commands
import re
import sqlite3
import cogs.dice_cog as dice_cog
import re

VERBOSE = False
result_re = re.compile('([^>]*)(?:\>([^>]*)\>([^>]*))?')
conn = sqlite3.connect("data/roll_tables.db")
cur = conn.cursor()

class RollTableCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    async def rolltable_game_autocomplete(self, 
                interaction: discord.Interaction, 
                current: str
                ) -> list[app_commands.Choice[str]]:
        options = [
            x[0] for x in 
            cur.execute("SELECT DISTINCT game FROM rolltables").fetchall()
            ]
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in options if current.lower() in choice.lower()
            ][:25]
    
    async def rolltable_table_autocomplete(self, 
                interaction: discord.Interaction, 
                current: str
                ) -> list[app_commands.Choice[str]]:
        if len(current) < -1:
            return []
        else:
            options = [x[0] 
                       for x in cur.execute(f"""
                            SELECT DISTINCT name FROM rolltables
                            WHERE game = '{interaction.namespace.game}'
                        """).fetchall()
                        ]
            return [
                app_commands.Choice(name=choice, value=choice)
                for choice in options if current.lower() in choice.lower()
                ][:25]
    
    @app_commands.command(description="Roll on a Table")
    @app_commands.autocomplete(table = rolltable_table_autocomplete)
    @app_commands.autocomplete(game = rolltable_game_autocomplete)
    async def rolltables(self, interaction, game:str, table:str):
        try:
            result, dice = _roll_table(game, table)
            await interaction.response.send_message(f"Rolled **{''.join(result)}**.")
        except Exception as e:
            await interaction.response.send_message(
                f"There was a problem... I had an {e.args[0]}")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(RollTableCog(bot))


# Non Discord Functions


def _roll_table(game, table):
    try:
        rows = cur.execute(f"""
                    SELECT * FROM rolltables 
                    WHERE 
                        game = '{game.strip()}' 
                    AND
                        name = '{table.strip()}'
                    """)
        
        rows = rows.fetchall()
        # print(rows)
        dietype = rows[0][2]
    except:
        raise Exception('Issue fetching table data')
    try:
        dieroll = dice_cog.parse(dietype)[2]
        # print(dietype, dieroll)
        rolled_row = [r for r in rows if r[3] == dieroll].pop()
        # print(rolled_row)
    except:
        raise Exception('Issue rolling a result')
    
    roll_result = []
    dicerolled = [dieroll]
    for section in rolled_row[4].split('>>'):
        if roll_result: roll_result.append(', ')
        
        rolled_cell, subgame, subtable = result_re.match(section).groups()
        roll_result.append(rolled_cell.strip())
        
        # print(rolled_cell, subgame, subtable)
        rolled_cell = [rolled_cell]
        if subgame and subtable:
            subresult, subdice = _roll_table(subgame, subtable)
            roll_result.extend(subresult)
            dicerolled.extend(subdice)
    
    return roll_result, dicerolled
    
if __name__ == '__main__':
    r, dices = _roll_table('Forgotten Ballad', 'Relic Type')
    print(r, dices)
    ''.join([x for x in r if x])