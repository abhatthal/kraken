import discord
from discord.ext import commands
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

        # On startup, continue tempbans (in case of server outage)
        channel = self.bot.get_channel(settings.LOGGING_CHANNEL)
        cursor.execute('SELECT member_id, unban_time FROM tempbans ORDER BY currency ASC')
        all_rows = cursor.fetchall()
        for row in all_rows:
            some_member = discord.Object(id = int(row[0]))
            time_to_wait = int(row[1]) - time.time()
            if time_to_wait < 0:
                time_to_wait = 0
            await asyncio.sleep(time_to_wait)
            logger.info(f'[UNBAN] {some_member.name}\n Moderator: {settings.BOT_NAME}')
                # eObj = await embed(ctx, colour = 0x05A000, author = f'[UNBAN] {some_member.name}')
                eObj = discord.Embed(title = '', type = 'rich')
                eObj.set_author(name = f'[UNBAN] {some_member.name}')
                eObj.colour = 0x05A000
                if eObj is not False:
                    await channel.send(embed = eObj)
                    await guild.unban(some_member)

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
    