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
    for cog in [x.split('.')[0] for x in os.listdir('cogs') if '__' not in x]:
        bot.load_extension(f'cogs.{cog}')

    bot.debug = bot.get_cog('Development').debug
    bot.database = bot.get_cog('Database')

bot.run(os.environ['BOT_TOKEN'], bot=True, reconnect=True)