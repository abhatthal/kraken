#!/usr/bin/env python3
import discord
import os
from discord.ext import commands

log = open('log', 'a')

bot = commands.Bot(command_prefix = '.', description = "A very honest discord bot")

@bot.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.environ['token'])

log.close()