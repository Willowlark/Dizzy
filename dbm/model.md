# roll_tables.db

Fully reset using `rolltables.py`. Different files feed the data in. These are rollable tables from ttrpgs.

## rolltables

Game, Name, and Dice get pulled out as distinct sets. They're duplicated across all rows of a Rollable Table. 

| Game | Game system this Rollable Table is in. |
| Name | Name of the Rollable Table |
| Dice | The die notation you need to roll on this Rollable Table |
| Roll | The number on the die roll represented in this row. |
| Result | The value rolled.|

A Result can roll another result using `Prefix>game>table >> ...`. The prefix will be applied to the result, and the game and table are used to roll another result. Multiple subtable rolls can be made using `>>` between them.

### Games

- `forgotten_ballad_tables.py`
    - Relic Tables
- `avatar_tables.py`
    - Names by Nation
    
# role_tables.db

Used with the role_cog to setup self role assignment.

## assignable

| guild | int ID of the Discord Guild the role is in.
| role | int ID of the role

## managers

| guild | int ID of the Discord Guild the user is in. You'd need multiple entries for the same user across multiple guilds.
| user | int ID of the user