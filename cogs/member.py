import discord
import random
import os
from discord.ext import commands
# Shamelessly took helper_files from Wall-E
# https://github.com/CSSS/wall_e/tree/master/helper_files
from helper_files.embed import embed
import helper_files.settings as settings


class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context = True)
    async def help(self, ctx, extension = None):
        # only show relevant cogs
        ignore = ['events.py']
        if extension == None:
            if not ('mod' in [role.name for role in ctx.author.roles]) and not ('GOD' in [role.name for role in ctx.author.roles]):
                ignore.append('moderator.py')
            if not ('GOD' in [role.name for role in ctx.author.roles]):
                ignore.append('admin.py')
        else:
            for filename in os.listdir('./cogs'):
                 if filename.endswith('.py'):
                     if extension.lower() not in filename:
                         ignore.append(filename)

        # get all the cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and filename not in ignore:
                # get commands from cog
                cog_name = filename[:-3].capitalize()
                cog = self.bot.get_cog(cog_name)
                cog_commands = cog.get_commands()

                # set image for thumbnail
                thumbnails = {
                    'Admin' : settings.ADMIN_IMG,
                    'Economy' : settings.ECONOMY_IMG,
                    'Member' : settings.MEMBER_IMG,
                    'Moderator' : settings.MODERATOR_IMG,
                    'Music' : settings.MUSIC_IMG
                }
                thumbnail = thumbnails.get(cog_name)
                if not thumbnail:
                    thumbnail = ''

                # send an embed for each cog
                eObj = await embed(ctx, title = f'{cog_name} Plugin Commands', thumbnail = thumbnail)   

                # determine command usage
                usage = {
                    # Admin
                    'load' : '[extension]',
                    'unload' : '[extension]',
                    'reload' : '[extension] ...',
                    'sayin' : '[channel] [message]',

                    # Economy
                    'set_balance' : '[amount] (optional member)',
                    'delete_account' : '(optional member)',
                    'check_balance' : '(optional member)',
                    'transfer' : '[member] [amount]',

                    # Member
                    '_8ball' : '[question]',
                    'echo' : '[message]',

                    # Moderator
                    'clear' : '(optional amount)',
                    'kick' : '[member] (optional reason)',
                    'ban' : '[member] (optional reason)',
                    'unban' : '[member]',
                    'warn' : '[member] (optional reason)',
                    'infractions' : '[member]',
                    'clear_infractions' : '[member]',
                    'clear_infraction' : '[infraction id]',
                    'give_bluecan' : '[member]',
                    'remove_bluecan' : '[member]',

                    # Music
                    'join' : '[member]',
                    'play' : '[search or url]',
                    'volume' : '[number]'
                }

                # print all commands and their corresponding descriptions for that cog
                for command in cog_commands:
                    if command.name != 'help' and command.name != '_8ball':
                        usage_string = usage.get(command.name)
                        if not usage_string:
                            usage_string = ''
                        if command.name == '_8ball':
                            eObj.add_field(name = f'{settings.COMMAND_PREFIX}{command.name[1:]} {usage_string}', value = command.description, inline = False)
                        else:
                            eObj.add_field(name = f'{settings.COMMAND_PREFIX}{command.name} {usage_string}', value = command.description, inline = False)
                        
                # only send embed if no parsing errors
                if eObj is not False:
                    await ctx.send(embed = eObj)



    @commands.command(description = 'returns bot latency')
    async def ping(self, ctx):
        eObj = await embed(ctx, description = f'Pong! {round(self.bot.latency * 1000)}ms', author = settings.BOT_NAME, avatar = settings.BOT_AVATAR)
        if eObj is not False:
            await ctx.send(embed = eObj)
    

    @commands.command(aliases=['8ball'], description = 'Ask a yes or no question, get an answer')
    async def _8ball(self, ctx, *, question):
        responses = [
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            'Yes - definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            "Don't count on it.",
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Very doubtful.'
        ]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


    @commands.command(description = 'returns how many members are on the server')
    async def membercount(self, ctx):
        id = self.bot.get_guild(ctx.guild.id)
        eObj = await embed(ctx, author = settings.BOT_NAME, avatar = settings.BOT_AVATAR, description = f'Member Count: {id.member_count}')
        if eObj is not False:
            await ctx.send(embed=eObj)
        
        
    @commands.command(description = 'repeats what you say')
    async def echo(self, ctx, *, msg : str):
        user = ctx.author.display_name
        avatar = ctx.author.avatar_url
        eObj = await embed(ctx, author = user, avatar = avatar, description = msg)
        if eObj is not False:
            await ctx.send(embed=eObj)


def setup(bot):
    bot.add_cog(Member(bot))