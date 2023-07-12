import pandas as pd
import numpy as np
from datetime import datetime
from sys import modules
from inspect import getmembers, isclass
from .core import Command

class CounterBase(Command):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tier = 'Server'
        
    def tier_check(self, op):
        if op == 'counter':
            return "Server"
        elif op == 'mycounter':
            return "User"
        elif op == 'globalcounter':
            return "Global"
    
    def target_index_search(self, message, tier, counter_matches):
        
        target_index = None
        for index, row in counter_matches.iterrows():
            if row['TIER'] == 'User' and tier == 'User':
                if row['CREATOR'] == message.author.name:
                    target_index = index
            elif row['TIER'] == 'Server' and tier == 'Server':
                if row['SERVER_NAME'] == message.guild.name:
                    target_index = index
            elif row['TIER'] == 'Global' and tier == 'Global':
                target_index = index
            
        return target_index

class CounterIncrement(CounterBase):

    async def action(self, message, match):
        command, op, target, amnt = match[1:]
        amnt = int(amnt)
        
        tier = self.tier_check(command)

        counter_matches = self.options[self.options['COUNTER_NAME'] == target]
        
        target_index = self.target_index_search(message, tier, counter_matches)

        if target_index is None:
            await message.channel.send("I'm not counting those right now.")
        elif op == 'add':
            self.options.loc[self.options.index==target_index, 'CNT']+=amnt
            self.options.loc[self.options.index==target_index, 'MODIFIED_BIT'] = True
            result = int(self.options.loc[self.options.index==target_index, 'CNT'])
            await message.channel.send(f"The **{target}** count is {result}.")
        elif op == 'sub':
            self.options.loc[self.options.index==target_index, 'CNT']-=amnt
            self.options.loc[self.options.index==target_index, 'MODIFIED_BIT'] = True
            result = int(self.options.loc[self.options.index==target_index, 'CNT'])
            await message.channel.send(f"The **{target}** count is {result}.")
    
class CounterCheck(CounterBase):
    
    async def action(self, message, match):
        command, op, target = match[1:]
        
        tier = self.tier_check(command)
        
        counter_matches = self.options[self.options['COUNTER_NAME'] == target]
        
        target_index = self.target_index_search(message, tier, counter_matches)

        if target_index is None:
            await message.channel.send("I'm not counting those right now.")
        else:
            result = int(self.options.loc[self.options.index==target_index, 'CNT'])
            await message.channel.send(f"The **{target}** count is {result}.")

class CounterSet(CounterBase):

    async def action(self, message, match):
        command, op, target, amnt = match[1:]
        amnt = int(amnt)
        
        tier = self.tier_check(command)
        
        counter_matches = self.options[self.options['COUNTER_NAME'] == target]
        
        target_index = self.target_index_search(message, tier, counter_matches)

        if target_index is None:
            idd = self.options['ID'].max()+1 if self.options['ID'].max() is not np.nan else 1
            x = {
                'ID': idd,
                'TIER': tier,
                'SERVER_NAME': message.guild.name,
                'CREATOR': message.author.name,
                'COUNTER_NAME': target,
                'CNT': amnt,
                'MODIFIED_BIT': True
            }
            x = pd.Series(x)
            self.options = self.options.append(x, ignore_index=True)
            target_index = self.options.index[-1]
        else:
            self.options.loc[self.options.index==target_index, 'CNT'] = amnt
            self.options.loc[self.options.index==target_index, 'MODIFIED_BIT'] = True
        
        result = int(self.options.loc[self.options.index==target_index, 'CNT'])
        await message.channel.send(f"The **{target}** count is now {result}!")

class CounterRemove(CounterBase):

    async def action(self, message, match):
        command, op, target = match[1:]
        
        tier = self.tier_check(command)
        
        counter_matches = self.options[self.options['COUNTER_NAME'] == target]
        
        target_index = self.target_index_search(message, tier, counter_matches)

        if target_index is None:
            await message.channel.send("I'm not counting those right now.")
        else:
            self.options.loc[self.options.index==target_index, 'RM'] = True
            await message.channel.send("No longer counting {}!".format(target))

class CounterList(CounterBase):

    async def action(self, message, match):
        matches = match[1:]
        if len(matches) == 3:
            command, op, allflag = matches
        elif len(matches) == 2:
            command, op = matches
            allflag = None
            
        tier = self.tier_check(command)
        
        lines = ["Here's what I have.\n", '```']
        series_lines = pd.Series()
        for index, row in self.options.iterrows():
            if row['TIER'] == 'User' and (tier == 'User' or allflag):
                if row['CREATOR'] == message.author.name:
                    series_lines = series_lines.append(pd.Series([row['CNT']], index=[row['COUNTER_NAME']]))
            elif row['TIER'] == 'Server' and (tier == 'Server' or allflag):
                if row['SERVER_NAME'] == message.guild.name:
                    series_lines = series_lines.append(pd.Series([row['CNT']], index=[row['COUNTER_NAME']]))
            elif row['TIER'] == 'Global' and (tier == 'Global' or allflag):
                series_lines = series_lines.append(pd.Series([row['CNT']], index=[row['COUNTER_NAME']]))
        
        lines.append(series_lines.to_string())
        lines.append('```')

        await message.channel.send("".join(lines))

# REFERENCE = {
#     'CounterIncrement' : CounterIncrement,
#     'CounterCheck' : CounterCheck,
#     'CounterSet' : CounterSet,
#     'CounterRemove' : CounterRemove,
#     'CounterList' : CounterList
# }

clsmembers = getmembers(modules[__name__], isclass)
REFERENCE = clsmembers