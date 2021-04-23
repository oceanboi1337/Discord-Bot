import discord
from discord.ext import commands

class Setup(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    async def initialize(self):
        await self.bot.get_cog('Database').initialize()
        for guild in self.bot.guilds:
            await self.roles(guild)
            await self.bot.database.get_guild(guild)

    async def roles(self, guild : discord.Guild):
        roles = {
            'Verified': {
                'color': discord.Color.blurple(),
                'hoist': True
            }
        }

        for role in roles:
            if role not in [role.name for role in guild.roles]:
                try:
                    await guild.create_role(name=role, color=role['color'], hoist=role['hoist'], reason='Bot Setup')
                except Exception as e:
                    await guild.system_channel.send(f'Error while creating roles: {e}')
                    return False
        return True

def setup(bot):
    bot.add_cog(Setup(bot))