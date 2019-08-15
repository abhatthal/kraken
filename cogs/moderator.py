import discord
from discord.ext import commands
from discord.utils import get
# Shamelessly took helper_files from Wall-E
# https://github.com/CSSS/wall_e/tree/master/helper_files
from helper_files.embed import embed
import sqlite3
from datetime import datetime # get time for db logging
import logging
import helper_files.settings as settings

logger = logging.getLogger('HonestBear')


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(description = "Clears messages 'clear [amount](optional)'")
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount=10):
        if 'mod' in [role.name.lower() for role in ctx.author.roles] or 'GOD' in [role.name.lower() for role in ctx.author.roles]:
            await ctx.channel.purge(limit = amount + 1)
        else:
            await ctx.send("Sorry, only mods can clear messages! <:Asami:610590675142049868>")


    @commands.command(description = "kick a user from server 'kick [@member] [reason](optional)'")
    # @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason = None):
        if member.id == self.bot.user.id:
            await ctx.send('Ouch ;-;')
        elif member.id == ctx.author.id:
            await ctx.send('Why are you hitting yourself?')
        elif 'mod' in [role.name.lower() for role in ctx.author.roles] or 'GOD' in [role.name.lower() for role in ctx.author.roles]:
            logger.info(f'[KICK] {member}\n Moderator: {ctx.author}\n Reason: {reason}\n')
            channel = self.bot.get_channel(607056829067034634) #logging
            eObj = await embed(ctx, colour = 0xFF0000, title = 'ATTENTION:', author = f'[KICK] {member}' ,
                avatar = member.avatar_url, description = 'Reason: ' + str(reason))
            if eObj is not False:
                await ctx.send(embed = eObj)
                await channel.send(embed = eObj)
                await member.kick(reason = reason)
        else:
            await ctx.send("Hey, don't kick anybirdie! <:Asami:610590675142049868>")


    @commands.command(description = "Ban a user from server 'ban [@member] [reason](optional)'")
    # @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        if member.id == self.bot.user.id:
            await ctx.send('no u')
        elif member.id == ctx.author.id:
            await ctx.send("Please don't ban yourself")
        elif 'mod' in [role.name.lower() for role in ctx.author.roles] or 'GOD' in [role.name.lower() for role in ctx.author.roles]:
            logger.info(f'[BAN] {member}\n Moderator: {ctx.author}\n Reason: {reason}\n')
            channel = self.bot.get_channel(607056829067034634) #logging
            eObj = await embed(ctx, colour = 0xFF0000, author = f'[BAN] {member}' ,
                avatar = member.avatar_url, description = 'Reason: ' + str(reason))
            if eObj is not False:
                await ctx.send(embed = eObj)
                await channel.send(embed = eObj)
                await member.ban(reason = reason)
        else:
            await ctx.send("Hey, don't ban anybirdie! <:Asami:610590675142049868>")


    @commands.command(description = "Unban a user from server 'unban [member#1234]'")
    # @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        if member == '<@608911590515015701>' or member == 'Honest Bear#9253':
            await ctx.send("Wait, am I banned? >.<")
        elif str(ctx.author.id) in member or str(ctx.author) == member:
            await ctx.send("You can't unban yourself silly")
        elif 'mod' in [role.name.lower() for role in ctx.author.roles] or 'GOD' in [role.name for role in ctx.author.roles]:
            channel = self.bot.get_channel(607056829067034634) #logging
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
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
            await ctx.send("You're not allowed to unban anybirdie! <:Asami:610590675142049868>")

    
    @commands.command(description = "give a user an infraction 'warn [@member] [reason](optional)'")
    # @commands.has_role('mod')
    async def warn(self, ctx, member : discord.Member, *, reason = None):
        if member.id == self.bot.user.id:
            await ctx.send('no u')
        elif member.id == ctx.author.id:
            await ctx.send("You can't warn yourself")
        elif 'mod' in [role.name.lower() for role in ctx.author.roles] or 'GOD' in [role.name for role in ctx.author.roles]:
            channel = self.bot.get_channel(607056829067034634) #logging
            logger.info(f'[WARN] {member}\n Moderator: {ctx.author}\n Reason: {reason}\n')
            eObj = await embed(ctx, colour = 0xFFA000, title = 'ATTENTION:', author = f'[WARN] {member}' ,
                avatar = member.avatar_url, description = str(reason), footer = 'Moderator Warning')
            if eObj is not False:
                await ctx.send(embed = eObj)
                await channel.send(embed = eObj)
                settings.c.execute(f"INSERT INTO infractions VALUES ({member.id}, '', {str(reason)}, {str(datetime.now())})")
                settings.conn.commit()
        else:
            await ctx.send("You're not allowed to warn anybirdie! <:Asami:610590675142049868>")


    @commands.command(description = "returns all a user's infractions 'infractions [@member]'")
    # @commands.has_role('mod')
    async def infractions(self, ctx, member : discord.Member):
        if 'mod' in [role.name.lower() for role in ctx.author.roles] or 'GOD' in [role.name for role in ctx.author.roles]:
            eObj = await embed(ctx, title = 'INFRACTIONS:', author = f'{member}' ,
                avatar = member.avatar_url, description = 'uuh, database broke. sorry')
            if eObj is not False:
                await ctx.send(embed = eObj)
        else:
            await ctx.send("You're not allowed to view infractions! <:Asami:610590675142049868>")


    @commands.command(description = "gives a user bluecan role 'blueify [@member]'")
    async def blueify(self, ctx, member : discord.Member):
        bluecan = get(ctx.guild.roles, id = 606911719217823745)
        if 'mod' in [role.name.lower() for role in ctx.author.roles] or 'GOD' in [role.name for role in ctx.author.roles]:
            eObj = await embed(ctx, title = 'Congrats!', author = f'{member}' ,
                avatar = member.avatar_url, description = "You're a bluecan now!")
            if eObj is not False:
                await ctx.send(embed = eObj)
            await member.add_roles(bluecan)
        else:
            await ctx.send("You can't turn toucans into bluecans! <:Asami:610590675142049868>")


    @commands.command(description = "removes a user's bluecan role 'blueify [@member]'")
    async def unblueify(self, ctx, member : discord.Member):
        bluecan = get(ctx.guild.roles, id = 606911719217823745)
        if 'mod' in [role.name.lower() for role in ctx.author.roles] or 'GOD' in [role.name for role in ctx.author.roles]:
            eObj = await embed(ctx, title = 'Sorry!', author = f'{member}' ,
                avatar = member.avatar_url, description = "Your bluecan role has been removed.")
            if eObj is not False:
                await ctx.send(embed = eObj)
            await member.remove_roles(bluecan)
        else:
            await ctx.send("You can't turn bluecans into toucans! <:Asami:610590675142049868>")


def setup(bot):
    bot.add_cog(Moderator(bot))