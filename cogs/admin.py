import discord
from discord.ext import commands
from os import listdir
import logging
import helper_files.settings as settings
logger = logging.getLogger(settings.BOT_NAME)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description = 'bot speaks in specified channel')
    async def sayin(self, ctx, channel : discord.TextChannel, *, msg : str):
        await channel.send(msg)


    @commands.command(description = 'loads an extension')
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')
        msg = f'[LOAD] cogs.{extension}\n'
        logger.info(f'{ctx.author.name}#{ctx.author.discriminator}: {msg}')
        await ctx.send(msg)
    
    
    @commands.command(description = 'unloads an extension')
    async def unload(self, ctx, extension):
        if extension == 'admin':
            raise commands.CommandError('Unloading admin is a REALLY bad idea')
        self.bot.unload_extension(f'cogs.{extension}')
        msg = f'[UNLOAD] cogs.{extension}\n'
        logger.info(f'{ctx.author.name}#{ctx.author.discriminator}: {msg}')
        await ctx.send(msg)
    
    
    @commands.command(description = 'reloads extensions')
    async def reload(self, ctx, *extensions):
        if len(extensions) == 0:
            raise commands.CommandError('Must pass at least one extension')
        if 'all' in extensions:
            for filename in listdir('./cogs'):
                 if filename.endswith('.py'):
                    try:
                        self.bot.unload_extension(f'cogs.{filename[:-3]}')
                        self.bot.load_extension(f'cogs.{filename[:-3]}')
                    except:
                        self.bot.load_extension(f'cogs.{filename[:-3]}')
                    msg = f'[RELOAD] cogs.{filename[:-3]}\n'
                    logger.info(f'{ctx.author.name}#{ctx.author.discriminator}: {msg}')
                    await ctx.send(msg)
        else:
            for extension in extensions:
                try:
                    self.bot.unload_extension(f'cogs.{extension}')
                    self.bot.load_extension(f'cogs.{extension}')
                except:
                    self.bot.load_extension(f'cogs.{extension}')
                msg = f'[RELOAD] cogs.{extension}\n'
                logger.info(f'{ctx.author.name}#{ctx.author.discriminator}: {msg}')
                await ctx.send(msg)


    @commands.command(description = 'bot goes offline')
    async def shutdown(self, ctx):
        logger.info(f'{ctx.author.name}#{ctx.author.discriminator}: Shut Down')
        await ctx.send("Shutting down!")
        await self.bot.logout()


    async def cog_check(self, ctx):
        user_roles = [role.name for role in sorted(ctx.author.roles, key=lambda x: int(x.position), reverse=True)]
        return settings.ADMIN in user_roles or ctx.author.id == settings.OWNER


def setup(bot):
    bot.add_cog(Admin(bot))