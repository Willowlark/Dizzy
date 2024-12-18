import discord
from discord.ext import commands
from discord import app_commands
from random import choice
import re
import cogs.dice_cog as dice_cog
import re
import yaml

DEBUG = False
VERBOSE = False

class MadlibCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.tableset = self._load_tables()
    
    async def source_autocomplete(self, 
                                          interaction: discord.Interaction, 
                                          current: str
                                          ) -> list[app_commands.Choice[str]]:
        choices = [c for c in self._all_sources() if current.lower() in c.lower()][:25]
        return [app_commands.Choice(name=choice, value=choice) for choice in choices]
    
    async def title_autocomplete(self, 
                                          interaction: discord.Interaction, 
                                          current: str
                                          ) -> list[app_commands.Choice[str]]:
        if len(current) < -1:
            return []
        else:
            options = self._all_titles(interaction.namespace.game)
            choices = [c for c in options if current.lower() in c.lower()][:25]
            return [app_commands.Choice(name=choice, value=choice) for choice in choices]
    
    @app_commands.command(description="Roll on a Table")
    @app_commands.autocomplete(game = source_autocomplete)
    @app_commands.autocomplete(table = title_autocomplete)
    async def rollon(self, interaction, game:str, table:str, number:int):
        try:
            table_id = self._find_table(game, table)
            results = []
            for i in range(number):
                results.append(self._yaml_table(table_id))
            result = '\n'.join(results)
            await interaction.response.send_message(f"Rolled:\n*{result}*.")
        except Exception as e:
            await interaction.response.send_message(
                f"There was a problem... I had an {e.args[0]}")

    @app_commands.command(description="Generate a Markdown Table")
    @app_commands.autocomplete(game = source_autocomplete)
    @app_commands.autocomplete(table = title_autocomplete)
    async def printtable(self, interaction, game:str, table:str):
        try:
            table_id = self._find_table(game, table)
            result = self._markdown(table_id)
            await interaction.response.send_message(f"Here's your table:\n\n### {table}\n\n```\n{result}\n```")
        except Exception as e:
            await interaction.response.send_message(
                f"There was a problem... I had an {e.args[0]}")
    
    def _load_tables(self):
        return yaml.safe_load(open('data/tables.yaml'))
    
    def _all_sources(self):
        return set([self.tableset[table][0]['source'] for table in self.tableset])
    
    def _all_titles(self,source_filter = None):
        if not source_filter:
            return set([self.tableset[table][0]['title'] for table in self.tableset])
        else: 
            choices = [self.tableset[table][0] for table in self.tableset]
            return [c['title'] for c in choices if source_filter.lower() in c['source'].lower()]
        
    def _find_table(self, source, title):
        return [table for table in self.tableset if self.tableset[table][0]['source'] == source and self.tableset[table][0]['title'] == title][0]
        
    def _yaml_table(self, table, log={}):
        REPLACE_PATTERN = f'<(.*?)#?(\d+)?>'
        # Search for Human Readable match from Table
        if table not in self.tableset:
            raise Exception("UnknownTableNameError")
        if DEBUG: print([x for x in self.tableset[table] if type(x) != dict])
        result = choice([x for x in self.tableset[table] if type(x) != dict])
        for replace_target, replace_id in re.findall(REPLACE_PATTERN, result):
            if replace_id not in log:
                r = self._yaml_table(replace_target, log)
                result = re.sub(REPLACE_PATTERN, r, result, count=1)
            else:
                result = re.sub(REPLACE_PATTERN, log[replace_id], result, count=1)
            
            if replace_id: log[replace_id] = r
        return result
    
    def _markdown(self, table):
        ops = [x for x in self.tableset[table] if type(x) != dict]
        op_cnt = len(ops)
        try:
            dimensions = self._die_codify(op_cnt)
            if type(dimensions) == int: dimensions = [1, dimensions]
        except:
            return f"Can't Make Table for {table} with {op_cnt} Options"

        cols = []
        for c in range(0, dimensions[0]):
            cols.append(ops[c*dimensions[1]:c*dimensions[1]+dimensions[1]])        
        
        # The 'd' column is automatically added through the dimension sizes.
        if dimensions[0] == 3: headers = '|d|1-2|3-4|5-6|'
        elif dimensions[0] == 2: headers = '|d|1-3|4-6|'
        else: 
            headers = '|'.join([f'{i}' for i in range(1,dimensions[0]+1)])
            headers = f'|d|{headers}|'
        divider = '|---'*(dimensions[0]+1) + '|' #+1 for the d column
        mdrows = []
        row_cnt = 0
        for i in zip(*cols):
            row_cnt+=1
            mdrows.append(f'|{row_cnt}|'+'|'.join(i)+'|')
        output = headers+'\n'+divider+'\n'
        output += '\n'.join(mdrows)
        # print(output)
        return output
        
    def _die_codify(self, op_cnt):
        for d in [20, 12, 10, 8, 6, 4, 3, 2]:
            if op_cnt % d == 0: # Even divides only, can't have fraction tables.
                slice_size = op_cnt/d
                if slice_size == 1: # Base Case, options fit in a single column.
                    return 1, d
                else: # d is the column size, die_codify for a row wise
                    nxt = self._die_codify(slice_size) 
                    if nxt[0] == 1: 
                        return nxt[1], d
                    else:
                        raise Exception("Weird Case Found, 3 dimensions")
        raise Exception(f"Can't Make Table for {op_cnt} Options")
    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(MadlibCog(bot))
    
if __name__ == '__main__':
    m = MadlibCog('bot')
    print(m._all_sources())
    print(m._all_titles('Forgotten Ballad'))
    print(m._find_table('Forgotten Ballad', 'Instrument'))
    print(m._yaml_table('forgotten_ballad_relic'))
    print(m._markdown('forgotten_ballad_weapon'))
    print(m._markdown('forgotten_ballad_instrument'))
    print(m._markdown('atla_air_nomad_names'))