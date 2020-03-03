import discord
from discord.ext import commands
from discord.utils import get
import time
from time import gmtime, strftime
from random import choice
import logging
import helper_files.settings as settings
import aiosqlite3
import asyncio # await asyncio.sleep()
logger = logging.getLogger('HonestBear')


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        # connect to SQL database
        db = await aiosqlite3.connect(settings.DATABASE)
        cursor = await db.cursor()
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS infractions(
            member_id INTEGER,
            infraction_id INTEGER, 
            infraction TEXT,
            warn_time INTEGER
            )
            ''')
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS tempbans(
            member_id INTEGER,
            tempban_id INTEGER,
            guild_id INTEGER,
            reason TEXT,
            unban_time INTEGER
            )
        ''')
        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS economy(
            member_id INTEGER,
            currency INTEGER,
            wait_time INTEGER
            )
            ''')            
        await db.commit()

        logger.info('Bot Online')
        print('Bot Online')

        # On startup, continue tempbans (in case of server outage)
        await cursor.execute('SELECT member_id, unban_time, guild_id FROM tempbans ORDER BY unban_time ASC')
        all_rows = await cursor.fetchall()

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
            eObj.colour = 0x3b745b
            if eObj is not False:
                # in the event that the user was manually unbanned, just remove from the tempban table
                try:
                    await guild.unban(user)
                    logger.info(f'[UNBAN] {user}\n Moderator: {settings.BOT_NAME}')
                    await logging_channel.send(embed = eObj)
                except:
                    pass
                await cursor.execute(f'DELETE FROM tempbans WHERE member_id = {row[0]}')
                await db.commit()
        # close connection
        await cursor.close()
        await db.close()        


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if not isinstance(error, commands.CommandNotFound) and not isinstance(error, commands.CheckFailure):
            await ctx.send(error)


    @commands.Cog.listener()
    async def on_message(self, message):
        # Don't read bot messages
        if not message.author.bot:
            ctx = await self.bot.get_context(message)
            # Event Messages outside of Debate
            if message.channel.id != settings.DEBATE_CHANNEL:
                bot_messages = []
                if 'aww man' in message.content.lower() or 'aw man' in message.content.lower():
                    bot_messages.append(await ctx.send('So we back in the mine'))
                elif 'creeper' in message.content.lower():
                    bot_messages.append(await ctx.send('aww man'))

                if 'owo' in message.content.lower():
                    bot_messages.append(await ctx.send("OwO What's this?"))

                if 'no u' in message.content.lower():
                    bot_messages.append(await ctx.send('NO U'))

                if 'uwu' in message.content.lower():
                    responses = ['urusai!', 'baka', 'uwu dattebayo']
                    bot_messages.append(await ctx.send(choice(responses)))

                if 'omae wa mo shindeiru' in message.content.lower() or 'お前はもう死んでいる' in message.content.lower():
                    bot_messages.append(await ctx.send('NANI?!'))

                # Event Messages are temporary
                for bot_message in bot_messages:
                    await bot_message.delete(delay = 5)
            
                # Suggestions Voting
                if message.channel.id in (settings.SUGGESTIONS_CHANNEL, settings.EMOJI_SUGGESTIONS_CHANNEL):
                    await message.add_reaction('✅')
                    await message.add_reaction('❌')

            # Auto Moderation
            warn = self.bot.get_command('warn')
            user_roles = [role.name for role in sorted(ctx.author.roles, key=lambda x: int(x.position), reverse=True)]
            # rules don't apply to mods
            if not settings.MODERATOR in user_roles and not settings.ADMIN in user_roles:
                # Check for bad words
                suffixes = ['', 's', 'z', ',', '.', '!', '?', '*', '**', '***', '||']
                prefixes = ['', ',', '*', '**', '***', '||']
                for bad_word in settings.BLACKLIST:
                    for suffix in suffixes:
                        for prefix in prefixes:
                            if prefix + bad_word + suffix in message.content.lower().split(' '):
                                await message.delete()
                                await ctx.invoke(warn, member = message.author, reason = 'Bad word usage', automod = True, message = message.content)
                                # at most one 'Bad word usage' warning per message
                                break

                # exceptions = [settings.DEBATE_CHANNEL, settings.RETARDVILLE_CHANNEL, settings.MEMES_CHANNEL, settings.ART_CHANNEL,
                #  settings.SUGGESTIONS_CHANNEL, settings.EMOJI_SUGGESTIONS_CHANNEL, settings.PROPER_CHANNEL,
                # settings.WEEB_CHANNEL, settings.MAGAUS_CHANNEL, settings.MUSIC_CHANNEL, settings.GENERAL_VC_CHANNEL,
                # settings.COOKING_CHANNEL, settings.GAMING_CHANNEL]
                # link_identifiers = ['www.', '.com', 'http://', 'https://']

                # Check for server invites
                if 'discord.gg/' in message.content.lower():
                    await message.delete()
                    await ctx.invoke(warn, member = message.author, reason = 'Posted an invite', automod = True, message = message.content)

                # Check for external links
                # if not message.channel.id in exceptions:
                #     for link_identifier in link_identifiers:
                #         if link_identifier in message.content.lower():
                #             await message.delete()
                #             await ctx.invoke(warn, member = message.author, reason = 'Posted a link', automod = True, message = message.content)
                #             break


def setup(bot):
    bot.add_cog(Events(bot))
    