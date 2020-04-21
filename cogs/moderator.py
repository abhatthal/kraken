import discord
from discord.ext import commands
from discord.utils import get
# Shamelessly took helper_files from Wall-E
# https://github.com/CSSS/wall_e/tree/master/helper_files
from helper_files.embed import embed
from helper_files.listOfRoles import getListOfUserPerms
import logging
import helper_files.settings as settings
import json
import aiosqlite3
import datetime
import time
import asyncio # await asyncio.sleep()
import typing # for clear command typing.Union
logger = logging.getLogger(settings.BOT_NAME)


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # for alarm command
        self.alarm_status = False
        self.channel_perms = []
    

    @commands.command(description = 'Clears messages in a particular channel')
    async def clear(self, ctx, arg1 : typing.Union[discord.Member, int] = None, amount = 10):
        member = None
        if type(arg1) == int:
            amount = arg1
        else:
            member = arg1

        def is_member(m):
            return m.author == member

        user_perms = await getListOfUserPerms(ctx)
        if 'manage_messages' in user_perms:
            if member:
                await ctx.channel.purge(limit = amount + 1, check = is_member)
            else:
                await ctx.channel.purge(limit = amount + 1)

            msg = f'I have deleted {amount} message'
            if amount == 1:
                msg = msg + '!'
            else:
                msg = msg + 's!'

            eObj = await embed(ctx, author = msg, avatar = settings.BOT_AVATAR)
            if eObj is not False:
                bot_message = await ctx.send(embed = eObj)
                await bot_message.delete(delay = 5)                
        else:
            await ctx.send(f'Sorry, only mods can clear messages! {settings.ASAMI_EMOJI}')


    @commands.command(description = 'Kick a user from the server')
    async def kick(self, ctx, member : discord.Member, *, reason = 'Unspecified'):
        user_perms = await getListOfUserPerms(ctx)
        if member.id == self.bot.user.id:
            await ctx.send('Ouch ;-;')
        elif member.id == ctx.author.id:
            await ctx.send('Why are you hitting yourself?')
        elif 'kick_members' in user_perms:
            channel = self.bot.get_channel(settings.LOGGING_CHANNEL)
            # embed to send user
            eObj = await embed(ctx, colour = 0x2D2D2D, author = f'{member} has been kicked',
                avatar = member.avatar_url, description = f'**Reason: **{reason}')
            # embed for logging channel
            content = [('User', f'<@{member.id}>'), ('Moderator', f'<@{ctx.author.id}>'), ('Reason', reason)]
            eObj_log = await embed(ctx, colour = 0xF04848, author = f'[KICK] {member}' ,
                avatar = member.avatar_url, content = content, inline = True)
            # log warning
            logger.info(f'[BAN] {member}\n Moderator: {ctx.author}\n Reason: {reason}')
            # send embeds if valid
            if eObj is not False:
                await ctx.send(embed = eObj)
            if eObj_log is not False:
                await channel.send(embed = eObj_log)
            # DM user that they've been kicked and why
            DMmsg = f"You've been kicked from {ctx.guild.name}!\n"
            DMmsg += f'Reason: "{reason}"'
            await member.send(DMmsg)
            # actually kick them
            await member.kick(reason = reason)
        else:
            await ctx.send(f"Hey, don't kick anybirdie! {settings.ASAMI_EMOJI}")


    @commands.command(description = 'Bans a member from the server')
    async def ban(self, ctx, member : discord.Member, *, reason = 'Unspecified', automod = False):
        user_perms = await getListOfUserPerms(ctx)
        if member.id == self.bot.user.id:
            await ctx.send('no u')
        elif member.id == ctx.author.id and not automod:
            await ctx.send("Please don't ban yourself")
        elif 'ban_members' in user_perms or automod:
            channel = self.bot.get_channel(settings.LOGGING_CHANNEL)
            mod_name = f'<@{self.bot.user.id}>' if automod else f'<@{ctx.author.id}>'
            # embed to send user
            eObj = await embed(ctx, colour = 0x2D2D2D, author = f'{member} has been banned',
                avatar = member.avatar_url, description = f'**Reason: **{reason}')
            # embed for logging channel
            content = [('User', f'<@{member.id}>'), ('Moderator', mod_name), ('Reason', reason)]
            eObj_log = await embed(ctx, colour = 0xF04848, author = f'[BAN] {member}' ,
                avatar = member.avatar_url, content = content, inline = True)
            # log warning
            logger.info(f'[BAN] {member}\n Moderator: {mod_name}\n Reason: {reason}')
            # send embeds if valid
            if eObj is not False:
                await ctx.send(embed = eObj)
            if eObj_log is not False:
                await channel.send(embed = eObj_log)
            # connect to database
            db = await aiosqlite3.connect(settings.DATABASE)
            cursor = await db.cursor()
            # clear infractions and economy
            await cursor.execute(f'DELETE FROM infractions WHERE member_id = {member.id}')
            await cursor.execute(f'DELETE FROM economy WHERE member_id = {member.id}')
            await db.commit()
            # DM user that they've been banned and why
            DMmsg = f"You've been banned from {ctx.guild.name}!\n"
            DMmsg += f'Reason: "{reason}"'
            await member.send(DMmsg)
            # ban member
            await member.ban(reason = reason)
        else:
            await ctx.send(f"Hey, don't ban anybirdie! {settings.ASAMI_EMOJI}")


    @commands.command(description = 'Unbans a user from the server')
    async def unban(self, ctx, *, member):
        user_perms = await getListOfUserPerms(ctx)
        if member == '<@608911590515015701>' or member == f'{settings.BOT_NAME}#9253':
            await ctx.send("Wait, am I banned? >.<")
        elif str(ctx.author.id) in member or str(ctx.author) == member:
            await ctx.send("You can't unban yourself silly")
        elif 'ban_members' in user_perms:
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
                    eObj = await embed(ctx, author = f'[UNBAN] {member}')
                    if eObj is not False:
                        await ctx.send(embed = eObj)
                        await channel.send(embed = eObj)
                    return
            await ctx.send("That user isn't banned")
        else:
            await ctx.send(f"You're not allowed to unban anybirdie! {settings.ASAMI_EMOJI}")


    @commands.command(description = 'Temporarily bans a member from the server')
    async def tempban(self, ctx, member : discord.Member, duration, *, reason = 'Unspecified', automod = False):
        user_perms = await getListOfUserPerms(ctx)
        if member.id == self.bot.user.id:
            await ctx.send('no u')
        elif member.id == ctx.author.id and not automod:
            await ctx.send("Please don't ban yourself")
        elif 'ban_members' in user_perms or automod:
            unit = ''
            if duration[:-1].isnumeric():
                if duration[-1].isalpha():
                    if duration[-1].lower() == 's':
                        time_seconds = int(duration[:-1])
                        unit = 'seconds'
                    elif duration[-1].lower() == 'm':
                        time_seconds = int(duration[:-1]) * 60
                        unit = 'minutes'
                    elif duration[-1].lower() == 'h':
                        time_seconds = int(duration[:-1]) * 60 * 60
                        unit = 'hours'
                    elif duration[-1].lower() == 'd':
                        time_seconds = int(duration[:-1]) * 60 * 60 * 24
                        unit = 'days'
                    else:
                        await ctx.send('Error: time unit not recognized')
                        return
                else:
                    time_seconds = int(duration)
            else:
                await ctx.send('Error: No duration specified')
                return
            unban_time = time.time() + time_seconds
            channel = self.bot.get_channel(settings.LOGGING_CHANNEL)
            # embed to send user
            duration = f'{duration[:-1]} {unit}'
            eObj = await embed(ctx, colour = 0x2D2D2D, author = f'{member} has been banned for {duration}',
                avatar = member.avatar_url, description = f'**Reason: **{reason}')
            # embed for logging channel
            mod_name = f'<@{self.bot.user.id}>' if automod else f'<@{ctx.author.id}>'
            content = [('User', f'<@{member.id}>'), ('Moderator', str(mod_name)), ('Reason', reason), ('Duration', duration, False)]
            eObj_log = await embed(ctx, colour = 0xF04848, author = f'[BAN] {member}' ,
                avatar = member.avatar_url, content = content, inline = True)
            # log warning
            logger.info(f'[BAN] {member}\n Moderator: {mod_name}\n Reason: {reason}\n Duration: {duration}')
            # send embeds if valid
            if eObj is not False:
                await ctx.send(embed = eObj)
            if eObj_log is not False:
                await channel.send(embed = eObj_log)
            # backup data in case of server outage
            # connect to database
            db = await aiosqlite3.connect(settings.DATABASE)
            cursor = await db.cursor()
            # get tempban_id (number of global tempbans + 1)
            await cursor.execute('SELECT COUNT(*) FROM tempbans')
            tempban_id = await cursor.fetchone()
            tempban_id = tempban_id[0] + 1
            # insert data
            await cursor.execute('''
            INSERT INTO tempbans(member_id, tempban_id, guild_id, reason, unban_time)
            VALUES(?, ?, ?, ?, ?)''', (member.id, tempban_id, ctx.guild.id, str(reason), unban_time))
            await db.commit()
            # DM user that they've been banned and why
            DMmsg = f"You've been banned from {ctx.guild.name}!\n"
            DMmsg += f'Reason: "{reason}"\n'
            DMmsg += f'Duration: {duration}'
            await member.send(DMmsg)
            # ban and unban after time
            await member.ban(reason = reason)
            await asyncio.sleep(time_seconds)
            logger.info(f'[UNBAN] {member}\n Moderator: {settings.BOT_NAME}')
            await ctx.guild.unban(member)
            await cursor.execute(f'DELETE FROM tempbans WHERE member_id = {member.id}')
            await db.commit()
            # close connection
            await cursor.close()
            await db.close()   
            eObj = await embed(ctx, author = f'[UNBAN] {member}')
            if eObj is not False:
                await channel.send(embed = eObj)
        else:
            await ctx.send(f"You're not allowed to ban anybirdie! {settings.ASAMI_EMOJI}")
                

    @commands.command(description = 'Give a user an infraction')
    async def warn(self, ctx, member : discord.Member, *, reason = 'Unspecified', automod = False, message = None):
        user_perms = await getListOfUserPerms(ctx)
        if member.id == self.bot.user.id:
            await ctx.send('no u')
        elif member.id == ctx.author.id and not automod:
            await ctx.send("You can't warn yourself")
        elif 'ban_members' in user_perms or automod:
            channel = self.bot.get_channel(settings.LOGGING_CHANNEL)
            # embed to send user
            eObj = await embed(ctx, colour = 0x2D2D2D, author = f'{member} has been warned',
                avatar = member.avatar_url, description = f'**Reason: **{reason}')
            # embed for logging channel
            mod_name = f'<@{self.bot.user.id}>' if automod else f'<@{ctx.author.id}>'
            content = [('User', f'<@{member.id}>'), ('Moderator', str(mod_name)), ('Reason', reason)]
            if automod and message:
                content.append(('Channel', f'<#{ctx.channel.id}>', False))
                content.append(('Message', message, False))
            eObj_log = await embed(ctx, colour = 0xFFA000, author = f'[WARN] {member}' ,
                avatar = member.avatar_url, content = content, inline = True)
            # log warning
            logger.info(f'[WARN] {member}\n Moderator: {mod_name}\n Reason: {reason}\n')
            # send embeds if valid
            if eObj is not False:
                await ctx.send(embed = eObj)
            if eObj_log is not False:
                await channel.send(embed = eObj_log)
            # connect to database
            db = await aiosqlite3.connect(settings.DATABASE)
            cursor = await db.cursor()
            # get infraction_id (number of global infractions + 1)
            await cursor.execute('SELECT infraction_id FROM infractions ORDER BY infraction_id DESC')
            infraction_id = await cursor.fetchone()
            if not infraction_id:
                infraction_id = 0
            else:
                infraction_id = infraction_id[0] + 1
            # insert data
            await cursor.execute('''
            INSERT INTO infractions(member_id, infraction_id, infraction, warn_time)
            VALUES(?, ?, ?, ?)''', ( member.id, infraction_id, str(reason), time.time() ))
            await db.commit()
            # Check how many infractions member has now
            await cursor.execute(f'SELECT warn_time FROM infractions WHERE member_id = {member.id}')
            all_rows = await cursor.fetchall()
            recent_infractions = 0
            for row in all_rows:
                if time.time() - row[0] <= 60 * 60:
                    recent_infractions += 1
            # if recent_infractions >= 5:
                # await ctx.invoke(self.ban, member, reason = 'Too many infractions', automod = True)
            if recent_infractions >= 4:
                await ctx.invoke(self.tempban, member, reason = 'Too many infractions', duration = '24h', automod = True)        
            # close connection
            await cursor.close()
            await db.close()   
        else:
            await ctx.send(f"You're not allowed to warn anybirdie! {settings.ASAMI_EMOJI}")


    @commands.command(description = "See all of a user's infractions")
    async def infractions(self, ctx, member : discord.Member = None):
        user_perms = await getListOfUserPerms(ctx)
        if member == None:
            member = ctx.author
        if 'ban_members' in user_perms or ctx.author.id == member.id:
            # connect to database
            db = await aiosqlite3.connect(settings.DATABASE)
            cursor = await db.cursor()
            # fetch data
            await cursor.execute(f'SELECT warn_time, infraction_id, infraction FROM infractions WHERE member_id = {member.id}')
            all_rows = await cursor.fetchall()
            msg = ''
            recent_infractions = 0
            for row in all_rows:
                msg += f"{datetime.datetime.utcfromtimestamp(row[0]).strftime('%Y-%m-%d %H:%M:%S')} UTC #{row[1]} {row[2]}\n"
                if time.time() - row[0] <= 60 * 60:
                    recent_infractions += 1
            if msg == '':
                msg = f'No infractions! {settings.ASAMI_EMOJI}'
            else:
                msg = f'Infractions in last hour: {recent_infractions}\n' + msg
            # return data
            eObj = await embed(ctx, title = 'Infractions:', author = member,
                avatar = member.avatar_url, description = msg, footer = 'More than 3 infractions in 1 hour = 24 hour ban')
            if eObj is not False:
                await ctx.send(embed = eObj)
            # close connection
            await cursor.close()
            await db.close()   
        else:
            await ctx.send(f"You're not allowed to view their infractions! {settings.ASAMI_EMOJI}")


    @commands.command(aliases = ['clearinfractions'], description = "removes all of a user's infractions")
    async def clear_infractions(self, ctx, member : discord.Member):
        user_perms = await getListOfUserPerms(ctx)
        if 'ban_members' in user_perms:
            # connect to database
            db = await aiosqlite3.connect(settings.DATABASE)
            cursor = await db.cursor()
            # clear infractions
            await cursor.execute(f'DELETE FROM infractions WHERE member_id = {member.id}')
            await db.commit()
            # close connection
            await cursor.close()
            await db.close()
            # log infraction clear
            logger.info(f'[CLEAR ALL] {member}\n Moderator: {ctx.author}\n')
            # send message
            eObj = await embed(ctx, title = 'All Infractions Cleared', author = f'{member}' ,
                avatar = member.avatar_url)
            if eObj is not False:
                await ctx.send(embed = eObj)
        else:
            await ctx.send(f"You're not allowed to clear infractions! {settings.ASAMI_EMOJI}")

        
    @commands.command(aliases = ['clearinfraction'], description = "removes a specific user infraction")
    async def clear_infraction(self, ctx, infraction_id : int):
        user_perms = await getListOfUserPerms(ctx)
        if 'ban_members' in user_perms:
            # connect to database
            db = await aiosqlite3.connect(settings.DATABASE)
            cursor = await db.cursor()
            # get member
            await cursor.execute((f'SELECT member_id FROM infractions WHERE infraction_id = {infraction_id}'))
            member_id = await cursor.fetchone()
            member_id = int(member_id[0])
            member = ctx.guild.get_member(member_id)
            # get infraction data
            await cursor.execute(f'SELECT warn_time, infraction_id, infraction FROM infractions WHERE infraction_id = {infraction_id}')
            all_rows = await cursor.fetchall()
            msg = ''
            for row in all_rows:
                msg += f"{datetime.datetime.utcfromtimestamp(row[0]).strftime('%Y-%m-%d %H:%M:%S')} UTC #{row[1]} {row[2]}\n"
            # clear infraction
            await cursor.execute(f'DELETE FROM infractions WHERE infraction_id = {infraction_id}')
            await db.commit()
            # close connection
            await cursor.close()
            await db.close()
            # log infraction clear
            logger.info(f'[CLEAR] {member}\n Infraction: #{infraction_id}\n Moderator: {ctx.author}\n')
            # return data
            eObj = await embed(ctx, title = f'Infraction #{infraction_id} Cleared', author = f'{member}' ,
                avatar = member.avatar_url, description = msg)
            if eObj is not False:
                await ctx.send(embed = eObj)
        else:
            await ctx.send(f"You're not allowed to clear infractions! {settings.ASAMI_EMOJI}")


    # @commands.command(aliases = ['givebluecan'], description = 'gives a user the Bluecan role')
    # async def give_bluecan(self, ctx, member : discord.Member):
    #     user_perms = await getListOfUserPerms(ctx)
    #     if 'manage_roles' in user_perms:
    #         bluecan = get(ctx.guild.roles, name = 'Bluecan')
    #         eObj = await embed(ctx, title = 'Congrats!', author = f'{member}' ,
    #             avatar = member.avatar_url, description = "You're a bluecan now!")
    #         if eObj is not False:
    #             await ctx.send(embed = eObj)
    #         await member.add_roles(bluecan)
    #     else:
    #         await ctx.send(f"You can't turn toucans into bluecans! {settings.ASAMI_EMOJI}")           


    # @commands.command(aliases = ['removebluecan'], description = "removes a user's Bluecan role")
    # async def remove_bluecan(self, ctx, member : discord.Member):
    #     user_perms = await getListOfUserPerms(ctx)
    #     if 'manage_roles' in user_perms:
    #         bluecan = get(ctx.guild.roles, name = 'Bluecan')
    #         eObj = await embed(ctx, title = 'Sorry!', author = member,
    #             avatar = member.avatar_url, description = 'Your bluecan role has been removed.')
    #         if eObj is not False:
    #             await ctx.send(embed = eObj)
    #         await member.remove_roles(bluecan)
    #     else:
    #         await ctx.send(f"You can't turn bluecans into toucans! {settings.ASAMI_EMOJI}")


    @commands.command(description = 'shhh...')
    async def mute(self, ctx, member : discord.Member):
        user_perms = await getListOfUserPerms(ctx)
        if 'manage_roles' in user_perms:
            channel = self.bot.get_channel(settings.LOGGING_CHANNEL)
            mute = get(ctx.guild.roles, name = 'Muted')
            eObj = await embed(ctx, colour = 0x2D2D2D, author = f'{member} has been muted',
                avatar = member.avatar_url)
            if eObj is not False:
                await ctx.send(embed = eObj)
            content = [('User', f'<@{member.id}>'), ('Moderator', str(ctx.author))]
            eObj_log = await embed(ctx, colour = 0xFFA000, author = f'[MUTE] {member}' ,
                avatar = member.avatar_url, content = content, inline = True)
            if eObj_log is not False:
                await channel.send(embed = eObj_log)
            logger.info(f'[MUTE] {member}\n Moderator: {ctx.author}\n')
            await member.add_roles(mute)
        else:
            await ctx.send(f"You can't mute people! {settings.ASAMI_EMOJI}")


    @commands.command(description = 'un-shhh...')
    async def unmute(self, ctx, member : discord.Member):
        user_perms = await getListOfUserPerms(ctx)
        if 'manage_roles' in user_perms:
            channel = self.bot.get_channel(settings.LOGGING_CHANNEL)
            mute = get(ctx.guild.roles, name = 'Muted')
            eObj = await embed(ctx, colour = 0x2D2D2D, author = f'{member} has been unmuted',
                avatar = member.avatar_url)
            if eObj is not False:
                await ctx.send(embed = eObj)
            content = [('User', f'<@{member.id}>'), ('Moderator', str(ctx.author))]
            eObj_log = await embed(ctx, colour = 0xFFA000, author = f'[UNMUTE] {member}' ,
                avatar = member.avatar_url, content = content, inline = True)
            if eObj_log is not False:
                await channel.send(embed = eObj_log)
            logger.info(f'[UNMUTE] {member}\n Moderator: {ctx.author}\n')
            await member.remove_roles(mute)
        else:
            await ctx.send(f"You can't unmute people! {settings.ASAMI_EMOJI}") 


    @commands.command(aliases = ['banword'], description = "Adds a word to blacklist")
    async def ban_word(self, ctx, word : str):
        word = word.lower()
        user_roles = [role.name for role in sorted(ctx.author.roles, key=lambda x: int(x.position), reverse=True)]
        if settings.MODERATOR in user_roles or ctx.author.id == settings.OWNER:
            if not word in settings.BLACKLIST:
                settings.BLACKLIST.append(word)
                settings.BLACKLIST.sort()
                with open('blacklist.json', 'w') as f:
                    json.dump(settings.BLACKLIST, f)
                    f.close()
                msg = f'The word "{word}" has been banned.'
            else:
                msg = 'Oops! That word is already banned.'
            user = ctx.author.display_name
            avatar = ctx.author.avatar_url
            eObj = await embed(ctx, title = 'Word Ban', author = user,
                avatar = avatar, description = msg)
            if eObj is not False:
                await ctx.send(embed = eObj)
            # log that word was banned
            logger.info(f'[BAN WORD] {word}\n Moderator: {ctx.author}\n')
        else:
            await ctx.send(f"You can't ban words! {settings.ASAMI_EMOJI}")


    @commands.command(aliases = ['unbanword'], description = "Removes a word from blacklist")
    async def unban_word(self, ctx, word : str):
        word = word.lower()
        user_roles = [role.name for role in sorted(ctx.author.roles, key=lambda x: int(x.position), reverse=True)]
        if settings.MODERATOR in user_roles or ctx.author.id == settings.OWNER:
            if word in settings.BLACKLIST:
                settings.BLACKLIST.remove(word)
                with open('blacklist.json', 'w') as f:
                    json.dump(settings.BLACKLIST, f)
                    f.close()
                msg = f'The word "{word}" has been unbanned.'
            else:
                msg = 'Oops! That word was not banned.'
            user = ctx.author.display_name
            avatar = ctx.author.avatar_url
            eObj = await embed(ctx, title = 'Word Unban', author = user,
                avatar = avatar, description = msg)
            if eObj is not False:
                await ctx.send(embed = eObj)
            # log that word was unbanned
            logger.info(f'[UNBAN WORD] {word}\n Moderator: {ctx.author}\n')
        else:
            await ctx.send(f"You can't unban words! {settings.ASAMI_EMOJI}")


    @commands.command(description = 'Enable/Disable sending messages')
    async def alarm(self, ctx):
        maintenance = True
        if maintenance and ctx.author.id != settings.OWNER:
            await ctx.send(f'This command is under construction. Sorry! {settings.ASAMI_EMOJI}\n')
        else:
            user_roles = [role.name for role in sorted(ctx.author.roles, key=lambda x: int(x.position), reverse=True)]
            user = ctx.author.display_name
            avatar = ctx.author.avatar_url
            if settings.MODERATOR in user_roles or ctx.author.id == settings.OWNER:
                if not self.alarm_status:
                    msg = 'The raid alarm has been pulled. Users without roles are unable to send messages.'
                    logger.info(f'[ALARM] Enabled\n Moderator: {user}\n')
                else:
                    msg = 'The raid alarm has been disabled. All users are now able to send messages again.'
                    logger.info(f'[ALARM] Disabled\n Moderator: {user}\n')
                # embed to send user
                eObj = await embed(ctx, colour = 0xF04848, title = 'Raid Alarm', author = user,
                    avatar = avatar, description = msg)
                # send embed if valid
                if eObj is not False:
                    await ctx.send(embed = eObj)
                # flip alarm status
                self.alarm_status = not self.alarm_status
                await ctx.send(ctx.guild.channels)
            else:
                await ctx.send(f"Only moderators can pull the alarm! {settings.ASAMI_EMOJI}\n")


def setup(bot):
    bot.add_cog(Moderator(bot))