import discord
from discord.ext import commands

from structs import Verification
import base64, asyncio, random, string, datetime

class Protection(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.__doc__ = 'Commands for verification and stuff'

    async def generate_verification(self, member : discord.Member):
        base = '*Hacker Voice* im in'
        salt = ''.join([random.choice(string.ascii_letters) for x in range(5)])
        plaintext = f'{base} {salt}'

        cipher = random.choice([16, 32, 64])
        encoded = None

        if cipher == 16:
            encoded = base64.b16encode(plaintext.encode())
        elif cipher == 32:
            encoded = base64.b32encode(plaintext.encode())
        elif cipher == 64:
            encoded = base64.b64encode(plaintext.encode())

        encoded = encoded.decode()

        return Verification(plaintext, encoded, cipher)

    @commands.command()
    @commands.guild_only()
    async def hint(self, ctx, challenge=None):
        hints = {
            'verification': 'https://www.youtube.com/watch?v=GVm35BlstjY'
        }

        if challenge in hints:
            await ctx.reply(hints[challenge])
        else:
            embed = discord.Embed(title=f'Challenge Hints', description='', color=discord.Color.blurple())
            for hint in hints:
                embed.add_field(name=hint, value=hints[hint])
            await ctx.reply(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def verify(self, ctx, *, code=None):
        role = discord.utils.get(ctx.guild.roles, name='Verified')
        if role not in ctx.author.roles:
            verification = await self.bot.database.get_verification(ctx.author)
            if verification.plaintext == code:
                await ctx.author.add_roles(role)
                await self.bot.database.remove_verification(ctx.author)
                await ctx.reply(f'You have been verified.')
            elif code == None:
                await ctx.reply(f'Decode `{verification.encoded}` and verify with `.verify <plaintext>` to access the server.\nUse `.hint` if you need a hint.')
            else:
                await ctx.reply(f'Wrong, try again.')
        else:
            await ctx.reply(f'You are already verified.')

    async def account_age(self, member : discord.Member, days=7):
        created_at = member.created_at
        account_age = datetime.datetime.utcnow() - created_at
        return account_age.days >= days

def setup(bot):
    bot.add_cog(Protection(bot))