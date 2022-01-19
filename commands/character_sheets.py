import numpy as np
import re
from sys import modules
from inspect import getmembers, isclass

import commands.rollparser as rollparser
from .core import Command

class FateAccelLoad(Command):
    
    async def action(self, message, match):
        # import IPython; IPython.embed()
        character = {}
        try:
            character['CHARACTER_NAME'] = re.search('^\*\*(.*?)\*\*', match[3]).group(1)#.replace('*', '')
            character['CHARACTER_SHORT_NAME'] = match[2]
            character['DEFAULT_DIE_CODE'] = '4dF'
            character['FATE_POINTS'] = int(re.search('\*\*Fate Points:\*\* *([0-9]+)', match[3]).group(1))
            
            s = re.search('\*\*Stress:\*\*((?: *\[.\])+)', match[3]).group(1).strip()
            character['STRESS'] = len([x for x in s[1:-1].split('] [') if x != ' '])
            character['CONSEQUENCE_2'] = re.search('2  Mild:(.*)\n', match[3]).group(1).strip()
            character['CONSEQUENCE_4'] = re.search('4  Moderate:(.*)\n', match[3]).group(1).strip()
            character['CONSEQUENCE_6'] = re.search('6  Severe:(.*)\n', match[3]).group(1).strip()
            
            s = re.search('\*\*Aspects\*\*((?:\n+\* .*)+)', match[3]).group(1).strip()
            character['ASPECT_1'], character['ASPECT_2'], character['ASPECT_3'], character['ASPECT_4'], character['ASPECT_5'] = [x.strip() for x in ''.join(s.split('*')).split('\n')]
            character['CAREFUL'] = int(re.search('Careful: *`([+-]?[0-9])`', match[3]).group(1))
            character['CLEVER'] = int(re.search('Clever: *`([+-]?[0-9])`', match[3]).group(1))
            character['FLASHY'] = int(re.search('Flashy: *`([+-]?[0-9])`', match[3]).group(1))
            character['FORCEFUL'] = int(re.search('Forceful: *`([+-]?[0-9])`', match[3]).group(1))
            character['QUICK'] = int(re.search('Quick: *`([+-]?[0-9])`', match[3]).group(1))
            character['SNEAKY'] = int(re.search('Sneaky: *`([+-]?[0-9])`', match[3]).group(1))
            
            # idd = self.options['ID'].max()+1 if self.options['ID'].max() is not np.nan else 1
            # character['ID'] = idd
            character['SERVER'] = message.guild.name
            character['MODIFIED_BIT'] = True
            
        except:
            await message.channel.send(f"I'm sorry, I didn't quite get that (T.T)")
        else:
            # print(character)
            self.options = self.options.append(character,ignore_index=True)
            await message.channel.send(f"Following character updated: `{match[2]}`.")

class FateAccelCheck(Command):
    
    async def action(self, message, match):
        alias = match[2]
        row = self.options[self.options['CHARACTER_SHORT_NAME'] == alias]
        if not row.empty:
            row = row.iloc[0]
            if row['SERVER'] == message.guild.name:
                stress =('[x] '*row['STRESS']+'[ ] '*(3-row['STRESS'])).strip()
                character_string = f"**{row['CHARACTER_NAME']}**\n\n**Fate Points:** {row['FATE_POINTS']}\n**Stress:** {stress}\n**Consequences:**\n2  Mild: {row['CONSEQUENCE_2']}\n4  Moderate: {row['CONSEQUENCE_4']}\n6  Severe: {row['CONSEQUENCE_6']}\n\n**Aspects**\n\n* {row['ASPECT_1']}\n* {row['ASPECT_2']}\n* {row['ASPECT_3']}\n* {row['ASPECT_4']}\n* {row['ASPECT_5']}\n\n**Approaches**\nCareful: `{row['CAREFUL']}`\nClever: `{row['CLEVER']}`\nFlashy: `{row['FLASHY']}`\nForceful: `{row['FORCEFUL']}`\nQuick: `{row['QUICK']}`\nSneaky: `{row['SNEAKY']}`"
                
                if len(match)==4: character_string = f"```{character_string}\n```"
                else: character_string = f">>> {character_string}"
                
                await message.channel.send(f"{alias}'s Character Sheet is as follows!\n{character_string}")
            else:
                await message.channel.send(f"{alias} isn't a Character I know, can you introduce me sometime? (^^)")
        else:
            await message.channel.send(f"{alias} isn't a Character I know, can you introduce me sometime? (^^)")

class CharacterList(Command):
    
    async def action(self, message, match):
        li = self.options[self.options['SERVER'] == message.guild.name][['CHARACTER_SHORT_NAME', 'CHARACTER_NAME']].rename(columns={'CHARACTER_SHORT_NAME':"Alias"}).set_index('Alias')
        await message.channel.send(f"I have the character sheets for these characters!\n ```{li}```")

class CharacterRoll(Command):
    
    async def action(self, message, match):
        alias = match[2]
        key = match[3]
        skey = re.sub(r'\w+', lambda m:m.group(0).upper(), key).replace(' ', '_')
        row = self.options[self.options['CHARACTER_SHORT_NAME'] == alias]
        if not row.empty:
            row = row.iloc[0]
            if row['SERVER'] == message.guild.name:
                value = row[skey]
                
                if type(value) == np.int64:
                    og, rolls, unmod = rollparser.parse(row['DEFAULT_DIE_CODE'])
                    total = value+unmod
                    m = f"{row['CHARACTER_SHORT_NAME']} rolled **{unmod}** *{rolls}*!\n\n Their `{key}` stat is **{value}**, so total is {unmod}+{value}=**{total}**!"
                    await message.channel.send(m)
                else:
                    try:
                        og, rolls, total = rollparser.parse(value)
                    except: 
                        await message.channel.send(f"How do I roll that?! XT")
                    else:
                        await message.channel.send(f"{row['CHARACTER_SHORT_NAME']} rolled `{og}` and got {total}!\nThe rolls were :*{rolls}*")
        else:
            await message.channel.send(f"I don't know if {alias} can do that...")

class CharacterMod(Command):
    
    async def action(self, message, match):
        alias = match[2]
        key = match[3]
        value = match[4]
        skey = re.sub(r'\w+', lambda m:m.group(0).upper(), key).replace(' ', '_')
        # import IPython; IPython.embed()
        row = self.options[self.options['CHARACTER_SHORT_NAME'] == alias]
        if not row.empty:
            row = row.iloc[0]
            if row['SERVER'] == message.guild.name:
                
                try: 
                    if self.options.dtypes[skey] == np.int64: value = int(value)
                    if self.options.dtypes[skey] == object: value = str(value)
                except ValueError:
                    await message.channel.send(f"I don't think that's what goes in that category...")
                else:
                    old_value = row[skey]
                    self.options.loc[self.options.index==row.name, skey] = value
                    self.options.loc[self.options.index==row.name, 'MODIFIED_BIT'] = True
                    await message.channel.send(f"{row['CHARACTER_SHORT_NAME']} had {old_value} in {key}, I changed it to {value}.")
            else:
                await message.channel.send(f"{alias} doesn't have that...")
        else:
            await message.channel.send(f"{alias} doesn't have that...")

# REFERENCE = {
#     'FateAccelLoad' : FateAccelLoad,
#     'FateAccelCheck' : FateAccelCheck,
#     'CharacterList' : CharacterList,
#     'CharacterRoll' : CharacterRoll,
#     'CharacterMod' : CharacterMod
# }

clsmembers = getmembers(modules[__name__], isclass)
REFERENCE = clsmembers