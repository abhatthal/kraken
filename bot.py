#!/usr/bin/env python3
import discord
import os
from discord.ext import commands

log = open('log', 'a')

bot = commands.Bot(command_prefix = '.', description = "A very honest discord bot")

@bot.command()
@commands.has_role('mod')
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    msg = f'load: cogs.{extension}\n'
    log.write(msg)
    log.flush()
    await ctx.send(msg)

@bot.command()
@commands.has_role('mod')
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    msg = f'unload: cogs.{extension}\n'
    log.write(msg)
    log.flush()
    await ctx.send(msg)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.environ['token'])

log.close()