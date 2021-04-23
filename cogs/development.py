import discord
from discord.ext import commands

import os

class Development(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx):
        embed = discord.Embed(title=f'⚙️ Cogs Manager', description='Reloading', color=discord.Color.blurple())

        cogs = [x.split('.')[0] for x in os.listdir('cogs') if '__' not in x]
        counter = 0

        await self.bot.get_cog('Osint').session.close()

        for cog in cogs:
            name = cog.split('.')[-1].capitalize()
            try:
                self.bot.reload_extension(f'cogs.{cog}')
                embed.add_field(name=f'✅ {name}', value='Success')
                counter += 1
            except commands.ExtensionNotLoaded:
                self.bot.load_extension(f'cogs.{cog}')
            except Exception as e:
                embed.add_field(name=f'❌ {name}', value=e)
        
        self.bot.debug = self.bot.get_cog('Development').debug
        self.bot.database = self.bot.get_cog('Database')
        
        await self.bot.database.initialize()
        
        embed.set_footer(text=f'{counter}/{len(cogs)} Cogs reloaded')
        
        await ctx.send(embed=embed)

    async def debug(self, text):
        await self.bot.get_channel(834929087822430228).send(text)

def setup(bot):
    bot.add_cog(Development(bot))