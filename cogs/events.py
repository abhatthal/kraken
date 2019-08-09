import discord
from discord.ext import commands
from time import gmtime, strftime

log = open('log', 'a')

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        log.write(' UTC\nLogged in as\n')
        log.write(self.bot.user.name + '\n')
        log.write(str(self.bot.user.id) + '\n')
        log.write('------\n')
        log.flush()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log.write(f'{member} has joined the server!\n')
        log.flush()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log.write(f'{member} has left the server!\n')
        log.flush()
        
def setup(bot):
    bot.add_cog(Events(bot))