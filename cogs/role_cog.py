import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from config import OWNER_ID

conn = sqlite3.connect("data/role_tables.db")
cur = conn.cursor()

VERBOSE = False

class RoleCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    # ------------------------------------------------
    
    async def roles_ac(self, 
                        interaction: discord.Interaction, 
                        current: str
                        ) -> list[app_commands.Choice[str]]:
        if manager_check(interaction.guild.id, interaction.user.id):
            options = [r for r in interaction.guild.roles if r.is_assignable()]
            choices = [r.name for r in options if current.lower() in r.name.lower()][:25]
            return [app_commands.Choice(name=choice, value=choice) for choice in choices]
        else: return [app_commands.Choice(name=choice, value=choice) for choice in [""]]
    
    @app_commands.command(description="Enable a Command Role")
    @app_commands.autocomplete(role = roles_ac)
    async def role_opt_enable(self, interaction, role:str):
        if manager_check(interaction.guild.id, interaction.user.id):
            role_id, ds_role = get_role_id_from_name(interaction, role)
            
            assignable = sql_fetch('role', 'assignable', interaction.guild.id)
            if role_id not in assignable:
                cur.execute(f"""INSERT OR IGNORE INTO assignable VALUES
                            ({interaction.guild.id},{role_id})""")
                conn.commit()
                await interaction.response.send_message(
                    f"{role} can now be self added by users.", ephemeral=True)
            else:
                cur.execute(f"""DELETE FROM assignable WHERE
                            guild = {interaction.guild.id} AND role={role_id}""")
                conn.commit()
                await interaction.response.send_message(
                    f"{role} can no longer be self added by users.", ephemeral=True)
        else:
            await interaction.response.send_message(
                f"Only role managers can add enable new roles to be added. Sorry!", ephemeral=True)

    # ------------------------------------------------

    async def add_roles_ac(self, 
                            interaction: discord.Interaction, 
                            current: str
                            ) -> list[app_commands.Choice[str]]:
        
        assignable = sql_fetch('role', 'assignable', interaction.guild.id)
        options = [r for r in interaction.guild.roles if r.id in assignable]
        choices = [r.name for r in options if current.lower() in r.name.lower()][:25]
        return [app_commands.Choice(name=choice, value=choice) for choice in choices]

    @app_commands.command(description="Add a Role")
    @app_commands.autocomplete(role = add_roles_ac)
    async def role_opt_in(self, interaction, role:str):
        role_id, ds_role = get_role_id_from_name(interaction, role)
        has_role = [r.id for r in interaction.user.roles if r.id == role_id]
        
        if not has_role: 
            await interaction.user.add_roles(ds_role)
            await interaction.response.send_message(
            f"Added role {ds_role.name}.", ephemeral=True)
        if has_role: 
            await interaction.user.remove_roles(ds_role)
            await interaction.response.send_message(
            f"Removed role {ds_role.name}.", ephemeral=True)

    # ------------------------------------------------

    async def manager_ac(self, 
                        interaction: discord.Interaction, 
                        current: str
                        ) -> list[app_commands.Choice[str]]:
        if manager_check(interaction.guild.id, interaction.user.id):
            options = [r for r in interaction.guild.members]
            choices = [r.display_name for r in options if current.lower() in r.name.lower() or current.lower() in r.display_name.lower()][:25]
            return [app_commands.Choice(name=choice, value=choice) for choice in choices]
        else: return [app_commands.Choice(name=choice, value=choice) for choice in [""]]

    @app_commands.command(description='Add a User who can config Roles')
    @app_commands.autocomplete(user = manager_ac)
    async def role_manager(self, interaction, user:str):
        if interaction.user.id == OWNER_ID:
            member = [m for m in interaction.guild.members if 
                      m.name == user or m.display_name == user]
            if member:
                managers = sql_fetch('user', 'managers', interaction.guild.id)
                member = member[0]
                print(member.id, managers)
                if member.id not in managers:
                    cur.execute(f"""INSERT OR IGNORE INTO managers VALUES
                                    ({interaction.guild.id},{member.id})""")
                    conn.commit()
                        
                    await interaction.response.send_message(
                        f"User {member.display_name} can now manage roles.", ephemeral=True)
                else:
                    cur.execute(f"""DELETE FROM managers WHERE
                                guild = {interaction.guild.id} AND user={member.id}""")
                    conn.commit()
                    await interaction.response.send_message(
                        f"User {member.display_name} can no longer manage roles.", ephemeral=True)
            else:
                await interaction.response.send_message(
                    f"I don't know who {user} is? ", ephemeral=True)
        else:
            await interaction.response.send_message(
                f"Only the owner can add or remove managers!", ephemeral=True)

# ----------------------------------------------------

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(RoleCog(bot))

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

def manager_check(guild_id, id):
    result = sql_fetch('user', 'managers', guild_id)
    if id in result or id == OWNER_ID: return True
    else: return False

def get_role_id_from_name(interaction, role):
    roles = interaction.guild.roles
    ds_role = [r for r in roles if r.name == role][0]
    role_id = ds_role.id
    return role_id, ds_role

# Non Discord Functions

