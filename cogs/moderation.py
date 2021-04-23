import discord
from discord.ext import commands

import asyncio, datetime

class Moderation(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.__doc__ = 'Commands for Staff'

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit : int, user : discord.User=None):
        if not (limit > 0 and limit <= 100):
            await ctx.reply('Limit has to be 1 - 100.')
            return

        messages = []
        async for message in ctx.channel.history(limit=limit, after=datetime.datetime.utcnow() - datetime.timedelta(days=14)):
            if user != None and message.author == user:
                messages.append(message)
                continue
            messages.append(message)

        try:
            await self.bot.database.log_command(ctx, [limit, user])
        except Exception as e:
            await ctx.reply(e)

        if len(messages) > 0:
            try:
                await ctx.channel.delete_messages(messages)
            except Exception as e:
                await ctx.send(e)

            tmp = await ctx.reply(f'Deleted {len(messages)} messages.')
            await asyncio.sleep(4)
            await tmp.delete()
        else:
            tmp = await ctx.reply(f'No messages to delete.')
            await asyncio.sleep(4)
            await tmp.delete()

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def prune(self, ctx, limit : int, user : discord.User=None):
        if not (limit > 0 and limit <= 100):
            await ctx.reply('Limit has to be 1 - 100')
            return

        await ctx.reply('Deleting messages...')
        counter = 0
        async for message in ctx.channel.history(limit=limit):
            try:
                await message.delete()
                counter += 1
                if counter % 5 == 0:
                    await asyncio.sleep(1)
            except Exception as e:
                print(e)
                #await ctx.send(e)
        tmp = await ctx.reply(f'Deleted {counter} messages.')
        await asyncio.sleep(4)
        await tmp.delete()
    
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(view_audit_log=True)
    async def history(self, ctx, member : discord.Member=None):
        if not member:
            member = ctx.author
        logs = await self.bot.database.get_audit_logs(member)
        page_amount = int(len(logs) / 10) + 1
        if not logs:
            await ctx.reply(f'No logs found for {member}.')
            return

        embed = discord.Embed(title=f'Command History', description=member, color=discord.Color.blurple())
        embed.set_thumbnail(url=member.avatar_url)

        for command, args, timestamp in logs:
            embed.add_field(name=f'{command} {args}', value=datetime.datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'), inline=False)

        embed.set_footer(text='Page {1}/{page_amount}, react with ◀️ or ▶️ to view more')
        
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx):
        try:
            position = ctx.channel.position
            clone = await ctx.channel.clone()
            await clone.edit(position=position)
            await ctx.channel.delete()
        except Exception as e:
            print(e)
            await ctx.reply(f'Failed to nuke channel: {e}')

def setup(bot):
    bot.add_cog(Moderation(bot))