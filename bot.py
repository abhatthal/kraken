#!/usr/bin/env python3
import discord
from discord.ext import commands
from os import environ

log = open("log", 'w')

bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_ready():
    log.write("Bot is ready.")
    log.flush()

@bot.event
async def on_member_join(member):
    log.write(f"{member} has joined the server!")
    log.flush()

@bot.event
async def on_member_remove(member):
    log.write(f"{member} has left the server!")
    log.flush()

bot.run(environ["token"])

log.close()