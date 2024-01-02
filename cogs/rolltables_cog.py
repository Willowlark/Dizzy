import discord
from discord.ext import commands
from discord import app_commands
from random import sample
import re
import sqlite3
import cogs.dice_cog as dice_cog
import re

VERBOSE = False
result_re = re.compile('([^>]*)(?:\>([^>]*)\>([^>]*))?')
conn = sqlite3.connect("data/rollable.db")
cur = conn.cursor()

class RollTableCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    async def rolltable_game_autocomplete(self, 
                                          interaction: discord.Interaction, 
                                          current: str
                                          ) -> list[app_commands.Choice[str]]:
        query = "SELECT DISTINCT database FROM rollable"
        options = [ x[0] for x in cur.execute(query).fetchall() ]
        choices = [c for c in options if current.lower() in c.lower()][:25]
        return [app_commands.Choice(name=choice, value=choice) for choice in choices]
    
    async def rolltable_table_autocomplete(self, 
                                          interaction: discord.Interaction, 
                                          current: str
                                          ) -> list[app_commands.Choice[str]]:
        if len(current) < -1:
            return []
        else:
            query = f""" SELECT DISTINCT table_name FROM rollable 
                WHERE database = '{interaction.namespace.game}' """
            options = [x[0]  for x in cur.execute(query).fetchall()]
            choices = [c for c in options if current.lower() in c.lower()][:25]
            return [app_commands.Choice(name=choice, value=choice) for choice in choices]
    
    @app_commands.command(description="Roll on a Table")
    @app_commands.autocomplete(table = rolltable_table_autocomplete)
    @app_commands.autocomplete(game = rolltable_game_autocomplete)
    async def rolltables(self, interaction, game:str, table:str):
        try:
            result = _roll_table(game, table)
            await interaction.response.send_message(f"Rolled *{''.join(result)}*.")
        except Exception as e:
            await interaction.response.send_message(
                f"There was a problem... I had an {e.args[0]}")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(RollTableCog(bot))


# Non Discord Functions


def _roll_table(database, table):
    try:
        tdata = cur.execute(f"""
                    SELECT *
                    FROM rollable WHERE 
                    database = '{database}' AND
                    table_name = '{table.strip()}'
                    """)
        
        tdata = tdata.fetchall()[0]
        _, db, table, diecode, prefix, postfix = tdata
        if prefix is None: prefix = ""
        if postfix is None: postfix = ""
        table = table.strip().lower().replace(' ', '_')
        roll = sample(dice_cog.faces(diecode),1)[0]
        print(tdata, table, roll)
        row_conn = sqlite3.connect(f"data/{db}.db")
        row_cur = row_conn.cursor()
        trows = row_cur.execute(f"""SELECT * FROM {table} WHERE roll={roll}""")
        roll, result, cnt_schema, cnt_tables = trows.fetchall()[0]
        
        if cnt_schema and cnt_tables:
            subtable = ""
            subtables = [x.strip() for x in cnt_tables.split('>>')]
            for subtab in subtables:
                subtable += _roll_table(cnt_schema, subtab)
                if len(subtables) > 1: subtable+=' '
        else: subtable = ""
        
        return f"{prefix}{result}{postfix}{subtable}"
    except IOError:
        raise Exception('Issue fetching table data')
    
if __name__ == '__main__':
    r = _roll_table('Avatar TTRPG', 'Fire Nation Names')
    # r = _roll_table('Forgotten Ballad', 'Relic')
    print(r)