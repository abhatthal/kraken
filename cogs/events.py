import discord
from discord.ext import commands
from time import gmtime, strftime
from random import choice
import logging
import helper_files.settings as settings
import sqlite3
logger = logging.getLogger('HonestBear')


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        # connect to SQL database
        db = sqlite3.connect(settings.DATABASE)
        cursor = db.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS infractions(
            member_id INTEGER,
            infraction_id INTEGER, 
            infraction TEXT,
            temp_ban INTEGER,
            date DATE
            )
            ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS economy(
            member_id INTEGER,
            currency INTEGER,
            wait_time INTEGER
            )
            ''')            
        db.commit()
        logger.info('Bot Online')
        print('Bot Online')


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if not isinstance(error, commands.CommandNotFound):
            await ctx.send(error)


    @commands.Cog.listener()
    async def on_message(self, message):
        # If a message is sent not in #debate and is not sent by the bot
        if message.channel.id != settings.DEBATE_CHANNEL and self.bot.user.id != message.author.id:
            if 'aww man' in message.content.lower() or 'aw man' in message.content.lower():
                await message.channel.send('So we back in the mine')
            elif 'creeper' in message.content.lower():
                await message.channel.send('aww man')

            if 'owo' in message.content.lower():
                await message.channel.send("OwO What's this?")

            if 'no u' in message.content.lower():
                await message.channel.send('NO U')

            if 'uwu' in message.content.lower():
                responses = ['urusai kono weebu yarou! >.<', 'damare!', 'kono baka', 'baka', 'uwu dattebayo']
                await message.channel.send(choice(responses))
        
            # allow people to vote by in certain channels
            if message.channel.id in (settings.SUGGESTIONS_CHANNEL, settings.EMOJI_SUGGESTIONS_CHANNEL):
                await message.add_reaction('✅')
                await message.add_reaction('❌')

def setup(bot):
    bot.add_cog(Events(bot))
    