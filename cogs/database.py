import discord
from discord.ext import commands

from structs import Verification, GuildSettings
import sqlite3, time

class Database(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

        self.con = sqlite3.connect(self.bot.config['database'])
        self.c = self.con.cursor()

    async def initialize(self):
        tables = {
            'CREATE TABLE IF NOT EXISTS verifications (guild TEXT, uid TEXT, plaintext TEXT, encoded TEXT, cipher INT, timestamp INT)',
            'CREATE TABLE IF NOT EXISTS guilds (id TEXT, verification INTEGER DEFAULT 0)',
            'CREATE TABLE IF NOT EXISTS audit_logs (guild TEXT, uid TEXT, command TEXT, args TEXT, timestamp INT)',
            'CREATE TABLE IF NOT EXISTS wallets (uid TEXT PRIMARY KEY, balance REAL DEFAULT 0)',
            'CREATE TABLE IF NOT EXISTS combo_categories(id INTEGER PRIMARY KEY, name TEXT, price INTEGER)',
            'CREATE TABLE IF NOT EXISTS combo_list (id INTEGER PRIMARY KEY AUTOINCREMENT, category INTEGER PRIAMRY KEY, login VARCHAR(255), password VARCHAR(255))',
        }

        for table in tables:
            try:
                self.c.execute(table)
            except Exception as e:
                await self.bot.get_cog('Development').debug(f'Database error `{table}`: {e}`')

        await self.bot.debug('Database initialized.')
        self.con.commit()

    async def get_guild(self, guild : discord.Guild):
        try:
            self.c.execute('SELECT * FROM guilds WHERE id=?', [guild.id])
            settings = self.c.fetchone()
            
            if settings:
                return GuildSettings(*settings)
            else:
                self.c.execute('INSERT INTO guilds (id) VALUES(?)', [guild.id])
                self.con.commit()
                return GuildSettings(guild.id, 0)
        except Exception as e:
            await self.bot.debug(e)

    async def add_verification(self, member : discord.Member, data : Verification):
        try:
            self.c.execute('INSERT INTO verifications VALUES (?, ?, ?, ?, ?, ?)', [member.guild.id, member.id, data.plaintext, data.encoded, data.cipher, int(time.time())])
            self.con.commit()
            return True
        except Exception as e:
            await self.bot.debug(e)

    async def get_verification(self, member : discord.Member):
        try:
            self.c.execute('SELECT plaintext, encoded, cipher FROM verifications WHERE guild=? AND uid=? ORDER BY timestamp DESC LIMIT 1', [member.guild.id, member.id])
            verification = self.c.fetchone()
            
            if verification:
                return Verification(*verification)
            else:
                verification = await self.bot.get_cog('Protection').generate_verification(member)
                await self.add_verification(member, verification)
                return verification
        except Exception as e:
            await self.bot.debug(e)
    
    async def remove_verification(self, member : discord.Member):
        try:
            self.c.execute('DELETE FROM verifications WHERE guild=? AND uid=?', [member.guild.id, member.id])
            self.con.commit()
        except Exception as e:
            await self.bot.debug(e)

    async def get_balance(self, member : discord.Member):
        try:
            self.c.execute('SELECT balance FROM wallets WHERE uid=?', [member.id])
            balance = self.c.fetchone()
            if balance:
                return balance[0]
            else:
                self.c.execute('INSERT INTO wallets (uid) VALUES (?)', [member.id])
                self.con.commit()
                return 0
        except Exception as e:
            await self.bot.debug(e)

    async def add_balance(self, member : discord.Member, amount : float):
        try:
            self.c.execute('UPDATE wallets SET balance=balance+? WHERE uid=?', [amount, member.id])
            self.con.commit()
            return True
        except Exception as e:
            await self.bot.debug(e)

def setup(bot):
    bot.add_cog(Database(bot))
