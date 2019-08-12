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
        channel = ctx.message.author.voice
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        if (channel == None):
            await ctx.send('[ERROR] You are not in a voice channel')
            return
        else:
            channel = channel.channel
        # if bot already in a voice channel, move to the vc of author
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await ctx.send(f'[JOIN] {channel}')

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        if voice and voice.is_connected():
            await ctx.send(f'[LEAVE] {voice.channel}')
            await voice.disconnect()
        else:
            await ctx.send('[ERROR] Bot is not in a voice channel')

        
def setup(bot):
    bot.add_cog(Audio(bot))