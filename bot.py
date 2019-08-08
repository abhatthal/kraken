#!/usr/bin/env python3
import discord
from discord.ext import commands
from os import environ

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print("Bot is ready.")

client.run(environ["token"])