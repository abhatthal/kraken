import discord
from discord.ext import commands
from discord.utils import get
import time
from time import gmtime, strftime
from random import choice
import logging
import helper_files.settings as settings
import sqlite3
import asyncio # await asyncio.sleep()
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
            date DATE
            )
            ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tempbans(
            member_id INTEGER,
            tempban_id INTEGER,
            guild_id INTEGER,
            reason TEXT,
            unban_time INTEGER
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

        # On startup, continue tempbans (in case of server outage)
        cursor.execute('SELECT member_id, unban_time, guild_id FROM tempbans ORDER BY unban_time ASC')
        all_rows = cursor.fetchall()

        logging_channel = self.bot.get_channel(settings.LOGGING_CHANNEL)

        for row in all_rows:
            # get guild and its banned members
            guild = self.bot.get_guild(row[2])
            banned_users = await guild.bans()
            # get banned member from guild by id
            for ban_entry in banned_users:
                user = ban_entry.user
                if user.id == row[0]:
                    break
            time_to_wait = int(row[1]) - time.time()
            if time_to_wait < 0:
                time_to_wait = 0
            await asyncio.sleep(time_to_wait)
            eObj = discord.Embed(title = '', type = 'rich')
            eObj.set_author(name = f'[UNBAN] {user}')
            eObj.colour = 0x05A000
            if eObj is not False:
                # in the event that the user was manually unbanned, just remove from the tempban table
                try:
                    await guild.unban(user)
                    logger.info(f'[UNBAN] {user}\n Moderator: {settings.BOT_NAME}')
                    await logging_channel.send(embed = eObj)
                except:
                    pass
                cursor.execute(f'DELETE FROM tempbans WHERE member_id = {row[0]}')
                db.commit()


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if not isinstance(error, commands.CommandNotFound) and not isinstance(error, commands.CheckFailure):
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
                responses = ['urusai!', 'baka', 'uwu dattebayo']
                await message.channel.send(choice(responses))
        
            # allow people to vote by in certain channels
            if message.channel.id in (settings.SUGGESTIONS_CHANNEL, settings.EMOJI_SUGGESTIONS_CHANNEL):
                await message.add_reaction('✅')
                await message.add_reaction('❌')

def setup(bot):
    bot.add_cog(Events(bot))
    