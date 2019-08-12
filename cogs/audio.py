import discord
from discord.ext import commands
# from discord import FFmpegPCMAudio
from discord.utils import get
import youtube_dl
import os

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

    @commands.command(pass_context=True)
    async def play(self, ctx, url : str):
        song_there = os.path.isfile('song.mp3')
        # try delete because if song is in use, will throw permissions error
        try:
            if song_there:
                os.remove('song.mp3')
        except PermissionError:
            await ctx.send('[ERROR] Music playing')
            return
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        # options for download
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        # download song
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        # rename downloaded song into song.mp3
        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                name = file
                os.rename(file, 'song.mp3')
                break
        # play the song
        voice.play(discord.FFmpegPCMAudio('song.mp3'))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        # Note: don't go above 0.5, very loud. 0.07 is good
        voice.source.volume = 0.07
        nname = name.rsplit('-', 2)
        await ctx.send(f'[PLAY] {nname}')
        
        
        
def setup(bot):
    bot.add_cog(Audio(bot))