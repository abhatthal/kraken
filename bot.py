#!/usr/bin/env python3
import discord
import random
from discord.ext import commands
from os import environ

log = open('log', 'w')

bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_ready():
    log.write('Bot is ready.')
    log.flush()

@bot.event
async def on_member_join(member):
    log.write(f'{member} has joined the server!')
    log.flush()

@bot.event
async def on_member_remove(member):
    log.write(f'{member} has left the server!')
    log.flush()

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = [
        'It is certain.',
        'It is decidedly so.',
        'Without a doubt.',
        'Yes - definitely.',
        'You may rely on it.',
        'As I see it, yes.',
        'Most likely.',
        'Outlook good.',
        'Yes.',
        'Signs point to yes.',
        'Reply hazy, try again.',
        'Ask again later.',
        'Better not tell you now.',
        'Cannot predict now.',
        'Concentrate and ask again.',
        "Don't count on it.",
        'My reply is no.',
        'My sources say no.',
        'Outlook not so good.',
        'Very doubtful.'
    ]
    await ctx.send(f'Question {question}\nAnswer: {random.choice(responses)}')

@bot.command()
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)

@bot.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

@bot.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)

bot.run(environ['token'])

log.close()