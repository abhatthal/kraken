#!/usr/bin/env python3
import discord
import os
from discord.ext import commands
import helper_files.settings as settings

bot = commands.Bot(command_prefix = '.', description = "A very honest discord bot")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.environ['token'])