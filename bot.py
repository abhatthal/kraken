#!/usr/bin/env python3
import discord
import random
from discord.ext import commands
from os import environ

log = open('log', 'w')

bot = commands.Bot(command_prefix = '.', description = "A very honest discord bot")

@bot.event
async def on_ready():
    log.write('Logged in as\n')
    log.write(bot.user.name + '\n')
    log.write(str(bot.user.id) + '\n')
    log.write('------\n')
    log.flush()

@bot.event
async def on_member_join(member):
    log.write(f'{member} has joined the server!\n')
    log.flush()

@bot.event
async def on_member_remove(member):
    log.write(f'{member} has left the server!\n')
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
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)

@bot.command()
@commands.has_any_role('mod', 609112079252717604)
async def kick(ctx, member : discord.Member, *, reason=None):
    msg = f'[KICK] {member.name}#{member.discriminator} {str(member.id)}\n Reason: {reason}\n'
    log.write(msg)
    log.flush()
    channel = bot.get_channel(609112292742660099) #logging
    await member.kick(reason=reason)
    await channel.send(msg)

@bot.command()
@commands.has_any_role('mod', 609112079252717604)
async def ban(ctx, member : discord.Member, *, reason=None):
    msg = f'[BAN] {member.name}#{member.discriminator} {str(member.id)}\n Reason: {reason}\n'
    log.write(msg)
    log.flush()
    channel = bot.get_channel(609112292742660099) #logging
    await member.ban(reason=reason)
    await channel.send(msg)

bot.run(environ['token'])

log.close()