#!/usr/bin/env python3
import discord
import os
from discord.ext import commands
import helper_files.settings as settings

bot = commands.Bot(command_prefix = settings.COMMAND_PREFIX, description = settings.DESCRIPTION)
bot.remove_command('help')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

if __name__ == '__main__':
    bot.run(os.environ['token'])