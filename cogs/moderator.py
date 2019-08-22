import discord
from discord.ext import commands
from discord.utils import get
# Shamelessly took helper_files from Wall-E
# https://github.com/CSSS/wall_e/tree/master/helper_files
from helper_files.embed import embed
import logging
import helper_files.settings as settings
import sqlite3
import datetime
import asyncio # await asyncio.sleep()
logger = logging.getLogger('HonestBear')


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(description = 'Clears messages in a particular channel')
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount=10):
        if 'mod' in [role.name for role in ctx.author.roles] or 'GOD' in [role.name for role in ctx.author.roles]:
            await ctx.channel.purge(limit = amount + 1)
        else:
            await ctx.send(f'Sorry, only mods can clear messages! {settings.ASAMI_EMOJI}')


    @commands.command(description = 'kick a user from the server')
    # @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason = None):
        if member.id == self.bot.user.id:
            await ctx.send('Ouch ;-;')
        elif member.id == ctx.author.id:
            await ctx.send('Why are you hitting yourself?')
        elif 'mod' in [role.name for role in ctx.author.roles] or 'GOD' in [role.name for role in ctx.author.roles]:
            logger.info(f'[KICK] {member}\n Moderator: {ctx.author}\n Reason: {reason}\n')
            channel = self.bot.get_channel(settings.LOGGING_CHANNEL)
            eObj = await embed(ctx, colour = 0xFF0000, author = f'[KICK] {member}' ,
                avatar = member.avatar_url, description = 'Reason: ' + str(reason))
            if eObj is not False:
                await ctx.send(embed = eObj)
                await channel.send(embed = eObj)
                await member.kick(reason = reason)
        else:
            await ctx.send(f"Hey, don't kick anybirdie! {settings.ASAMI_EMOJI}")


    @commands.command(description = 'Ban a user from the server')
    # @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        if member.id == self.bot.user.id:
            await ctx.send('no u')
        elif member.id == ctx.author.id:
            await ctx.send("Please don't ban yourself")
        elif 'mod' in [role.name for role in ctx.author.roles] or 'GOD' in [role.name for role in ctx.author.roles]:
            logger.info(f'[BAN] {member}\n Moderator: {ctx.author}\n Reason: {reason}\n')
            channel = self.bot.get_channel(settings.LOGGING_CHANNEL)
            eObj = await embed(ctx, colour = 0xFF0000, author = f'[BAN] {member}' ,
                avatar = member.avatar_url, description = 'Reason: ' + str(reason))
            if eObj is not False:
                await ctx.send(embed = eObj)
                await channel.send(embed = eObj)
                await member.ban(reason = reason)
        else:
            await ctx.send(f"Hey, don't ban anybirdie! {settings.ASAMI_EMOJI}")


    @commands.command(description = 'Unban a user from the server')
    # @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        if member == '<@608911590515015701>' or member == f'{settings.BOT_NAME}#9253':
            await ctx.send("Wait, am I banned? >.<")
        elif str(ctx.author.id) in member or str(ctx.author) == member:
            await ctx.send("You can't unban yourself silly")
        elif 'mod' in [role.name for role in ctx.author.roles] or 'GOD' in [role.name for role in ctx.author.roles]:
            channel = self.bot.get_channel(settings.LOGGING_CHANNEL)
            banned_users = await ctx.guild.bans()
            # Check if member is valid
            if '#' in member:
                member_name, member_discriminator = member.split('#')
            else:
                raise commands.CommandError('Invalid member passed')
            # unban if in banned users list
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    logger.info(f'[UNBAN] {member}\n Moderator: {ctx.author}')
                    eObj = await embed(ctx, colour = 0x05A000, author = f'[UNBAN] {member}')
                    if eObj is not False:
                        await ctx.send(embed = eObj)
                        await channel.send(embed = eObj)
                        await ctx.guild.unban(user)
                    return
            await ctx.send("That user isn't banned")
        else:
            await ctx.send(f"You're not allowed to unban anybirdie! {settings.ASAMI_EMOJI}")


    @commands.command(description = 'bans a member for a specified amount of time')
    async def tempban(self, ctx, time : str, member : discord.Member):
        if member.id == self.bot.user.id:
            await ctx.send('no u')
        elif member.id == ctx.author.id:
            await ctx.send("Please don't ban yourself")
        elif 'mod' in [role.name for role in ctx.author.roles] or 'GOD' in [role.name for role in ctx.author.roles]:
            channel = self.bot.get_channel(settings.LOGGING_CHANNEL)
            msg = ''
            if time[:-1].isnumeric():
                if time[-1].isalpha():
                    if time[-1].lower() == 's':
                        time_seconds = int(time[:-1])
                    elif time[-1].lower() == 'm':
                        time_seconds = int(time[:-1]) * 60
                    elif time[-1].lower() == 'h':
                        time_seconds = int(time[:-1]) * 60 * 60
                    elif time[-1].lower() == 'd':
                        time_seconds = int(time[:-1]) * 60 * 60 * 24
                    else:
                        await ctx.send('Error: Time unit not recognized')
                        return
                else:
                    time_seconds = int(time)
            else:
                await ctx.send('Error: No time specified')
                return
            eObj = await embed(ctx, colour = 0xFF0000, author = f'[TEMPBAN] {member}' ,
                    avatar = member.avatar_url, description = 'Reason: ' + str(reason), footer = f'Banned until: {time.ctime(time.time() + time_seconds)}')
                if eObj is not False:
                    await ctx.send(embed = eObj)
                    await channel.send(embed = eObj)
                    await member.ban(reason = reason)
            await ctx.guild.ban(member)
            await asyncio.sleep(time_seconds)
            await ctx.guild.unban(member)
    

    @commands.command(description = 'give a user an infraction')
    # @commands.has_role('mod')
    async def warn(self, ctx, member : discord.Member, *, reason = None):
        if member.id == self.bot.user.id:
            await ctx.send('no u')
        elif member.id == ctx.author.id:
            await ctx.send("You can't warn yourself")
        elif 'mod' in [role.name for role in ctx.author.roles] or 'GOD' in [role.name for role in ctx.author.roles]:
            channel = self.bot.get_channel(settings.LOGGING_CHANNEL)
            logger.info(f'[WARN] {member}\n Moderator: {ctx.author}\n Reason: {reason}\n')
            eObj = await embed(ctx, colour = 0xFFA000, title = 'ATTENTION:', author = f'[WARN] {member}' ,
                avatar = member.avatar_url, description = str(reason), footer = 'Moderator Warning')
            if eObj is not False:
                await ctx.send(embed = eObj)
                await channel.send(embed = eObj)
                # connect to database
                db = sqlite3.connect(settings.DATABASE)
                cursor = db.cursor()
                # get infraction_id (number of global infractions + 1)
                cursor.execute('SELECT COUNT(*) FROM infractions')
                infraction_id = cursor.fetchone()[0] + 1
                # insert data
                cursor.execute('''
                INSERT INTO infractions(member_id, infraction_id, infraction, date)
                VALUES(?, ?, ?, ?)''', (member.id, infraction_id, str(reason), str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
                db.commit()
        else:
            await ctx.send(f"You're not allowed to warn anybirdie! {settings.ASAMI_EMOJI}")


    @commands.command(description = "returns all a user's infractions")
    # @commands.has_role('mod')
    async def infractions(self, ctx, member : discord.Member):
        if 'mod' in [role.name for role in ctx.author.roles] or 'GOD' in [role.name for role in ctx.author.roles] or ctx.author.id == member.id:
            # connect to database
            db = sqlite3.connect(settings.DATABASE)
            cursor = db.cursor()
            # fetch data
            cursor.execute(f'SELECT date, infraction_id, infraction FROM infractions WHERE member_id = {member.id}')
            all_rows = cursor.fetchall()
            msg = ''
            for row in all_rows:
                msg += f'{row[0]} #{row[1]} {row[2]}\n'
            if msg == '':
                msg = f'No infractions! {settings.ASAMI_EMOJI}'
            # return data
            eObj = await embed(ctx, title = 'INFRACTIONS:', author = member,
                avatar = member.avatar_url, description = msg)
            if eObj is not False:
                await ctx.send(embed = eObj)
        else:
            await ctx.send(f"You're not allowed to view infractions! {settings.ASAMI_EMOJI}")


    @commands.command(description = "removes all of a user's infractions")
    # @commands.has_role('mod')
    async def clear_infractions(self, ctx, member : discord.Member):
        if 'mod' in [role.name for role in ctx.author.roles] or 'GOD' in [role.name for role in ctx.author.roles]:
            # connect to database
            db = sqlite3.connect(settings.DATABASE)
            cursor = db.cursor()
            # clear infractions
            cursor.execute(f'DELETE FROM infractions WHERE member_id = {member.id}')
            db.commit()
            # return data
            eObj = await embed(ctx, title = 'All Infractions Cleared', author = f'{member}' ,
                avatar = member.avatar_url)
            if eObj is not False:
                await ctx.send(embed = eObj)
        else:
            await ctx.send(f"You're not allowed to clear infractions! {settings.ASAMI_EMOJI}")

        
    @commands.command(description = "removes a specific user infraction")
    # @commands.has_role('mod')
    async def clear_infraction(self, ctx, infraction_id : int):
        if 'mod' in [role.name for role in ctx.author.roles] or 'GOD' in [role.name for role in ctx.author.roles]:
            # connect to database
            db = sqlite3.connect(settings.DATABASE)
            cursor = db.cursor()
            # get member
            cursor.execute((f'SELECT member_id FROM infractions WHERE infraction_id = {infraction_id}'))
            member_id = int(cursor.fetchone()[0])
            member = ctx.guild.get_member(member_id)
            # get infraction data
            cursor.execute(f'SELECT date, infraction_id, infraction FROM infractions WHERE infraction_id = {infraction_id}')
            all_rows = cursor.fetchall()
            msg = ''
            for row in all_rows:
                msg += f'{row[0]} #{row[1]} {row[2]}\n'
            # clear infraction
            cursor.execute(f'DELETE FROM infractions WHERE infraction_id = {infraction_id}')
            db.commit()
            # return data
            eObj = await embed(ctx, title = f'Infraction #{infraction_id} Cleared', author = f'{member}' ,
                avatar = member.avatar_url, description = msg)
            if eObj is not False:
                await ctx.send(embed = eObj)
        else:
            await ctx.send(f"You're not allowed to clear infractions! {settings.ASAMI_EMOJI}")


    @commands.command(description = 'gives a user the Bluecan role')
    async def give_bluecan(self, ctx, member : discord.Member):
        bluecan = get(ctx.guild.roles, id = 606911719217823745)
        if 'mod' in [role.name for role in ctx.author.roles] or 'GOD' in [role.name for role in ctx.author.roles]:
            eObj = await embed(ctx, title = 'Congrats!', author = f'{member}' ,
                avatar = member.avatar_url, description = "You're a bluecan now!")
            if eObj is not False:
                await ctx.send(embed = eObj)
            await member.add_roles(bluecan)
        else:
            await ctx.send(f"You can't turn toucans into bluecans! {settings.ASAMI_EMOJI}")


    @commands.command(description = "removes a user's Bluecan role")
    async def remove_bluecan(self, ctx, member : discord.Member):
        bluecan = get(ctx.guild.roles, id = 606911719217823745)
        if 'mod' in [role.name for role in ctx.author.roles] or 'GOD' in [role.name for role in ctx.author.roles]:
            eObj = await embed(ctx, title = 'Sorry!', author = f'{member}' ,
                avatar = member.avatar_url, description = 'Your bluecan role has been removed.')
            if eObj is not False:
                await ctx.send(embed = eObj)
            await member.remove_roles(bluecan)
        else:
            await ctx.send(f"You can't turn bluecans into toucans! {settings.ASAMI_EMOJI}")


def setup(bot):
    bot.add_cog(Moderator(bot))