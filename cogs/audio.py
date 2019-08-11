import discord
from discord.ext import commands

class Audio(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def join(self, ctx):
        channel = ctx.message.author.voice.voice_channel
        await self.bot.join_voice_channel(channel)

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        server = ctx.message.server
        voice_client = self.bot.voice_client_in(server)
        await voice_client.disconnect()
        
def setup(bot):
    bot.add_cog(Audio(bot))