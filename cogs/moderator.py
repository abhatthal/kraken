import discord
from discord.ext import commands
import logging
logging.basicConfig(filename = 'bot.log', level = logging.INFO, format='%(asctime)s %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')

class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        """remove last n messages 'clear [n]'"""

        await ctx.channel.purge(limit=amount)


    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        """kick a user from server 'kick [@member] [reason](optional)'"""

        if member.id == self.bot.user.id:
            await ctx.send('Ouch ;-;')
        elif member.id == ctx.author.id:
            await ctx.send('Why are you hitting yourself?')
        elif ctx.message.author.server_permissions.kick_members:
            msg = f'[KICK] {member}\n Moderator: {ctx.author}\n Reason: {reason}\n'
            logging.info(msg)
            channel = self.bot.get_channel(607056829067034634) #logging
            await member.kick(reason=reason)
            await channel.send(msg)
            await ctx.send(msg)
        else:
            raise commands.CommandError("Sorry, you don't have permission to do that.")


    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        """Ban a user from server 'ban [@member] [reason](optional)'"""

        if member.id == self.bot.user.id:
            await ctx.send('no u')
        elif member.id == ctx.author.id:
            await ctx.send("Please don't ban yourself")
        elif ctx.message.author.server_permissions.ban_members:
            msg = f'[BAN] {member}\n Moderator: {ctx.author}\n Reason: {reason}\n'
            logging.info(msg)
            channel = self.bot.get_channel(607056829067034634) #logging
            await member.ban(reason=reason)
            await channel.send(msg)
            await ctx.send(msg)
        else:
            raise commands.CommandError("Sorry, you don't have permission to do that.")          


    @commands.command()
    async def unban(self, ctx, *, member):
        """Unban a user from server 'unban [member#1234]'"""

        if member == '<@608911590515015701>' or member == 'Honest Bear#9253':
            await ctx.send("Wait, am I banned? >.<")
        elif str(ctx.author.id) in member or str(ctx.author) == member:
            await ctx.send("You can't unban yourself silly")
        elif ctx.message.author.server_permissions.ban_members:
            channel = self.bot.get_channel(607056829067034634) #logging
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    msg = f'[UNBAN] {member}\n Moderator: {ctx.author}'
                    logging.info(msg)
                    await ctx.guild.unban(user)
                    await channel.send(msg)
                    await ctx.send(msg)
                    return
        else:
            raise commands.CommandError("Sorry, you don't have permission to do that.")                


def setup(bot):
    bot.add_cog(Moderator(bot))