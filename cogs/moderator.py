import discord
from discord.ext import commands
# Shamelessly took helper_files from Wall-E
# https://github.com/CSSS/wall_e/tree/master/helper_files
from helper_files.embed import embed
import logging
logging.basicConfig(filename = 'bot.log', level = logging.INFO, format='%(asctime)s %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')

class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount=10):
        """remove last n messages 'clear [n]'"""

        await ctx.channel.purge(limit = amount + 1)


    @commands.command()
    # @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason = None):
        """kick a user from server 'kick [@member] [reason](optional)'"""

        if member.id == self.bot.user.id:
            await ctx.send('Ouch ;-;')
        elif member.id == ctx.author.id:
            await ctx.send('Why are you hitting yourself?')
        elif 'mod' in [role.name.lower() for role in ctx.author.roles] or 'GOD' in [role.name.lower() for role in ctx.author.roles]:
            logging.info(f'[KICK] {member}\n Moderator: {ctx.author}\n Reason: {reason}\n')
            channel = self.bot.get_channel(607056829067034634) #logging

            eObj = await embed(ctx, colour = 0xFF0000, title = 'ATTENTION:', author = f'[KICK] {member}' ,
                avatar = member.avatar_url, footer = 'User Kicked')
            if eObj is not False:
                await ctx.send(embed = eObj)
                await channel.send(embed = eObj)
                await member.kick(reason = reason)
        else:
            await ctx.send("Hey, don't kick anybirdie! <:Asami:610590675142049868>")


    @commands.command()
    # @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        """Ban a user from server 'ban [@member] [reason](optional)'"""

        if member.id == self.bot.user.id:
            await ctx.send('no u')
        elif member.id == ctx.author.id:
            await ctx.send("Please don't ban yourself")
        elif 'mod' in [role.name.lower() for role in ctx.author.roles] or 'GOD' in [role.name.lower() for role in ctx.author.roles]:
            logging.info(f'[BAN] {member}\n Moderator: {ctx.author}\n Reason: {reason}\n')
            channel = self.bot.get_channel(607056829067034634) #logging

            eObj = await embed(ctx, colour = 0xFF0000, title = 'ATTENTION:', author = f'[BAN] {member}' ,
                avatar = member.avatar_url, footer = 'User Banned')
            if eObj is not False:
                await ctx.send(embed = eObj)
                await channel.send(embed = eObj)
                await member.ban(reason = reason)
        else:
            await ctx.send("Hey, don't ban anybirdie! <:Asami:610590675142049868>")


    @commands.command()
    # @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """Unban a user from server 'unban [member#1234]'"""

        if member == '<@608911590515015701>' or member == 'Honest Bear#9253':
            await ctx.send("Wait, am I banned? >.<")
        elif str(ctx.author.id) in member or str(ctx.author) == member:
            await ctx.send("You can't unban yourself silly")
        elif 'mod' in [role.name.lower() for role in ctx.author.roles] or 'GOD' in [role.name.lower() for role in ctx.author.roles]:
            channel = self.bot.get_channel(607056829067034634) #logging
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    logging.info(f'[UNBAN] {member}\n Moderator: {ctx.author}')

                    eObj = await embed(ctx, colour = 0x05A000, title = 'ATTENTION:', author = f'[UNBAN] {member}' ,
                        avatar = member.avatar_url, footer = 'User Unbanned')
                    if eObj is not False:
                        await ctx.send(embed = eObj)
                        await channel.send(embed = eObj)
                        await ctx.guild.unban(user)
                    return
        else:
            await ctx.send("You're not allowed to unban anybirdie! <:Asami:610590675142049868>")

    
    @commands.command()
    # @commands.has_role('mod')
    async def warn(self, ctx, member : discord.Member, *, reason = None):
        """give a user an infraction 'warn [@member] [reason](optional)"""

        if member.id == self.bot.user.id:
            await ctx.send('no u')
        elif member.id == ctx.author.id:
            await ctx.send("You can't warn yourself")
        elif 'mod' in [role.name.lower() for role in ctx.author.roles] or 'GOD' in [role.name.lower() for role in ctx.author.roles]:
            channel = self.bot.get_channel(607056829067034634) #logging
            logging.info(f'[WARN] {member}\n Moderator: {ctx.author}\n Reason: {reason}\n')
            
            eObj = await embed(ctx, colour = 0xFFA000, title = 'ATTENTION:', author = f'[WARN] {member}' ,
                avatar = member.avatar_url, description = str(reason), footer = 'Moderator Warning')
            if eObj is not False:
                await ctx.send(embed = eObj)
                await channel.send(embed = eObj)
        else:
            await ctx.send("You're not allowed to warn anybirdie! <:Asami:610590675142049868>")


def setup(bot):
    bot.add_cog(Moderator(bot))