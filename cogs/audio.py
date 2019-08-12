import discord
import youtube_dl
import os
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
from os import system

class Audio(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context = True, brief = 'bot joins the voice channel of the user')
    async def join(self, ctx):
        global voice
        try:
            channel = ctx.message.author.voice.channel
        except:
            await ctx.send(f'[ERROR] You are not in a voice channel')
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        # if bot already in a voice channel, move to the vc of author
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()        
        # disconnect and reconnect, bug fix    
        await voice.disconnect()

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await ctx.send(f'[JOIN] {channel}')


    @commands.command(pass_context = True, brief = 'bot leaves a voice chat if in one')
    async def leave(self, ctx):
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        if voice and voice.is_connected():
            await ctx.send(f'[LEAVE] {voice.channel}')
            await voice.disconnect()
        else:
            await ctx.send('[ERROR] Bot is not in a voice channel')
    

    @commands.command(pass_context = True, brief = "This will play a song 'play [url]'")
    async def play(self, ctx, url : str):
        song_there = os.path.isfile('song.mp3')
        try:
            if song_there:
                os.remove('song.mp3')
        except PermissionError:
            await ctx.send('[ERROR] Music playing')
            return
        voice = get(self.bot.voice_clients, guild = ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        await ctx.send('[PLAY] Downloading song')
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        await ctx.send('[PLAY] Song downloaded')

        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                name = file
                os.rename(file, 'song.mp3')
                break

        voice.play(discord.FFmpegPCMAudio('song.mp3'))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.volume = 100
        voice.is_playing()
        nname = name.rsplit('-', 2)
        await ctx.send(f'Now Playing: {nname}')
        
        
def setup(bot):
    bot.add_cog(Audio(bot))