import discord
from discord.ext import commands

import random

class Events(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.MissingPermissions):
            await ctx.reply(err)
        elif isinstance(err, commands.MissingRequiredArgument):
            await ctx.reply(f'Missing required argument `{err.param.name}` Usage: `{ctx.command.usage}`')
        elif isinstance(err, commands.BadArgument):
            await ctx.reply(err)
        elif isinstance(err, commands.NotOwner):
            await ctx.reply(err)
        elif isinstance(err, commands.CommandOnCooldown):
            await ctx.reply(err)
        elif isinstance(err, commands.MissingRole):
            await ctx.reply(err)

    @commands.Cog.listener()
    async def on_guild_join(self, guild : discord.Guild):
        if guild.system_channel == None:
            channel = random.choice(guild.text_channels)
            await channel.send(f'{guild.owner.mention} No system channel is set.')
        
        await self.bot.get_cog('Setup').initialize()

    @commands.Cog.listener()
    async def on_member_join(self, member : discord.Member):
        settings = await self.bot.database.get_guild(member.guild)
        if settings.verification == 1:
            verification = await self.bot.database.get_verification(member)
            await member.guild.system_channel.send(f'Welcome {member.mention}, decode `{verification.encoded}` and verify with `.verify <plaintext>` to access the server.\nUse `.hint` if you need a hint.')
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} Ready!')

        await self.bot.get_cog('Setup').initialize()

def setup(bot):
    bot.add_cog(Events(bot))