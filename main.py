import discord
from discord.ext import commands

import json, os

with open('config.json', 'r') as f:
    config = json.load(f)

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=config['prefix'], description='Willy Wonka', intents=intents)
bot.config = config
bot.remove_command('help')

if __name__ == '__main__':
    for cog in config.get('cogs'):
        bot.load_extension(cog)

    bot.debug = bot.get_cog('Development').debug
    bot.database = bot.get_cog('Database')

bot.run(os.environ['BOT_TOKEN'], bot=True, reconnect=True)