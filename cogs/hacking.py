import discord
from discord.ext import commands

import aiofile
import asyncio, os, sqlite3, time

class Hacking(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.__doc__ = 'L33t Hacker commands'

    @commands.command(description='Views the hacker bank of a user', usage='.bank <user>')
    @commands.has_role('Elite Hacker')
    async def bank(self, ctx, member : discord.Member=None):
        if not member:
            member = ctx.author

        balance = await self.bot.database.get_balance(member)
        embed = discord.Embed(title=f'🕵️ Hacker Bank 🕵️', description=f'{member}', color=discord.Color.blurple())
        embed.set_thumbnail(url='https://static3.bigstockphoto.com/4/7/3/large1500/374131855.jpg')
        embed.add_field(name=f'💸 Hacker Coins: ${balance}', value=f'** **', inline=False)

        await ctx.send(embed=embed)

    @commands.command(description='Give hacker coins to a user', usage='.give <user> <amount>')
    @commands.has_role('Elite Hacker')
    async def give(self, ctx, member : discord.Member, amount : int):
        balance = await self.bot.database.get_balance(ctx.author)
        if member == ctx.author:
            await ctx.reply(f'You can\'t give yourself hacker coins.')
            return
            
        if amount > 0 and balance >= amount:
            if await self.bot.database.add_balance(ctx.author, -amount):
                if await self.bot.database.add_balance(member, amount):
                    await ctx.reply(f'Finished transfering hacker coins :detective:')
            else:
                await ctx.reply(f'Failed to transfer hacker coins. :pensive:')
        else:
            await ctx.reply(f'You don\'t have enough hacker coins.')

def setup(bot):
    bot.add_cog(Hacking(bot))