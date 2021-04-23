import discord
from discord.ext import commands

import random, inspect

class Essentials(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.__doc__ = 'Commands like this one'

    @commands.command(description='Shows a list of available commands')
    async def help(self, ctx, cog=None, cmd=None):
        if not cog:
            embed = discord.Embed(title=f'Command Categories', description='.help <category> to view more details', color=discord.Color.blurple())
            for category in self.bot.cogs:
                if not self.bot.cogs[category].__doc__:
                    continue
                else:
                    embed.add_field(name=category, value=self.bot.cogs[category].__doc__, inline=False)
            await ctx.send(embed=embed)

        elif cog.capitalize() in self.bot.cogs:
            if not cmd:
                embed = discord.Embed(title=f'{cog.capitalize()} Commands', description='', color=discord.Color.blurple())
                for command in self.bot.walk_commands():
                    if command.cog_name == cog.capitalize():
                        embed.add_field(name=command.name, value=command.description)
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Essentials(bot))