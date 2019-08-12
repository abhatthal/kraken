import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get

class Audio(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        if not channel:
            await ctx.send("You are not connected to a voice channel")
        # if bot already in a voice channel, move to the vc of author
        else if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        global voice
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        if voice:
            voice.disconnect()
        else:
            await ctx.send("Bot is not in a voice channel")
        
def setup(bot):
    bot.add_cog(Audio(bot))