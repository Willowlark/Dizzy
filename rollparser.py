import random
import re
import numexpr

def _adv_roll(match):
    n, s, t = match.groups()
    n = int(n) if n else 1
    s = int(s)
    
    rolls = []
    for x in range(0, n):
        roll1 = random.randint(1, s)
        roll2 = random.randint(1, s)
        higher = roll1 if roll1 >= roll2 else roll2
        lower = roll1 if roll1 < roll2 else roll2
        if t == 'a': higher = f"**{higher}**"
        if t == 'd': lower = f"**{lower}**"
        rolls.append(f"({higher},{lower})")
    return f"({'+'.join([str(x) for x in rolls])})"

def _top_roll(match):
    n, s, cnt = match.groups()
    n = int(n) if n else 1
    s = int(s)
    cnt = int(cnt) if int(cnt) > 0 else 1
    
    rolls = []
    for x in range(0, n):
        roll = random.randint(1, s)
        rolls.append(roll)
    
    rolls = sorted(rolls,reverse=True)
    rolls = [str(x) for x in rolls]
    cnt = cnt if cnt < len(rolls) else len(rolls)
    rolls = [f"**{x}**" for x in rolls[:cnt]]+rolls[cnt:]
    return f"({'+'.join(rolls)})"

def _basic_roll(match):
    print(match.groups())
    n, s = match.groups()
    n = int(n) if n else 1
    s = int(s)
    
    rolls = []
    for x in range(0, n):
        roll = random.randint(1, s)
        rolls.append(roll)
    return f"({'+'.join([str(x) for x in rolls])})"
    
def _fudge_roll(match):
    n = match.groups()[0]
    n = int(n) if n else 4
    
    sides = [-1, -1, 0, 0, 1, 1]
    rolls = []
    for x in range(0, n):
        roll = sides[random.randint(0, 5)]
        rolls.append(roll)
    
    return f"({'+'.join([str(x) for x in rolls])})"
    
def parse(diestring):
    
    # Parse Dice notation
    rawstring = re.sub('(\d?|\d+)d(\d+)(a|d)', _adv_roll, diestring)
    rawstring = re.sub('(\d?|\d+)d(\d+)\^(\d+)', _top_roll, rawstring)
    rawstring = re.sub('(\d?|\d+)d(\d+)', _basic_roll, rawstring)
    rawstring = re.sub('(\d?|\d+)dF', _fudge_roll, rawstring)
    
    # Compress Advantage/Disadvantage before doing math, removing Bolding and unused roll
    evalstring = re.sub('\(\*\*([0-9]+)\*\*,[0-9]+\)|\([0-9]+,\*\*([0-9]+)\*\*\)', r"\1\2",rawstring)
    # Remove the dropped rolls from the Top roll notation
    evalstring = re.sub('(?<=\d\*\*)((?:\+\d+)+)',r'',evalstring) 
    # Removes all bolded numbers and replaces with the raw number
    evalstring = re.sub('\*\*(\d+)\*\*', r'\1', evalstring)
    
    print(evalstring)
    total = int(numexpr.evaluate(evalstring))
    
    return diestring, rawstring, total