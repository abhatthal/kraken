import discord
from discord.ext import commands
import logging
import helper_files.settings as settings
import sqlite3
logger = logging.getLogger('HonestBear')


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description = 'bot speaks in specified channel')
    @commands.has_role('GOD')
    async def sayin(self, ctx, channel : discord.TextChannel, *, msg : str):
        await channel.send(msg)

    @commands.command(description = 'loads an extension')
    @commands.has_role('GOD')
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')
        msg = f'[LOAD] cogs.{extension}\n'
        logger.info(msg)
        await ctx.send(msg)
    
    
    @commands.command(description = 'unloads an extension')
    @commands.has_role('GOD')
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        msg = f'[UNLOAD] cogs.{extension}\n'
        logger.info(msg)
        await ctx.send(msg)
    
    
    @commands.command(description = 'reloads an extension')
    @commands.has_role('GOD')
    async def reload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        self.bot.load_extension(f'cogs.{extension}')
        msg = f'[RELOAD] cogs.{extension}\n'
        logger.info(msg)
        await ctx.send(msg)


    @commands.command(description = 'bot goes offline')
    @commands.has_role('GOD')
    async def shutdown(self, ctx):
        db = sqlite3.connect(settings.DATABASE)
        db.close()
        logger.info(f'{self.author} : Shut Down')
        await ctx.send("Shutting down!")
        await self.bot.logout()


def setup(bot):
    bot.add_cog(Admin(bot))