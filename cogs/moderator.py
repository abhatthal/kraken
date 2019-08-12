import discord
from discord.ext import commands
import logging
logging.basicConfig(filename = 'bot.log', level = logging.INFO, format='%(asctime)s %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')

class Moderator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(brief = "remove last n messages 'clear [n]'")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        await ctx.channel.purge(limit=amount)


    @commands.command(brief = "kick a user from server 'kick [@member] [reason](optional)'")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        msg = f'[KICK] {member.mention}\n Reason: {reason}\n'
        logging.info(msg)
        channel = self.bot.get_channel(607056829067034634) #logging
        await member.kick(reason=reason)
        await channel.send(msg)
        await ctx.send(msg)


    @commands.command(brief = "Ban a user from server 'ban [@member] [reason](optional)'")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        msg = f'[BAN] {member.mention}\n Reason: {reason}\n'
        logging.info(msg)
        channel = self.bot.get_channel(607056829067034634) #logging
        await member.ban(reason=reason)
        await channel.send(msg)
        await ctx.send(msg)


    @commands.command(brief = "Unban a user from server 'unban [member#1234]'")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        channel = self.bot.get_channel(607056829067034634) #logging
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                msg = f'[UNBAN] {member}\n'
                logging.info(msg)
                await ctx.guild.unban(user)
                await channel.send(msg)
                await ctx.send(msg)
                return


def setup(bot):
    bot.add_cog(Moderator(bot))