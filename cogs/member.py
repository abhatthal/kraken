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
    async def help(self, ctx):
        # only show relevant cogs
        ignore = ['events.py']
        if not ('mod' in [role.name for role in ctx.author.roles]) and not ('GOD' in [role.name for role in ctx.author.roles]):
            ignore.append('moderator.py')
        if not ('GOD' in [role.name for role in ctx.author.roles]):
            ignore.append('admin.py')

        # get images
        admin = 'http://icons.iconarchive.com/icons/alecive/flatwoken/512/Apps-Terminal-Pc-104-icon.png'
        member = 'https://www.airfieldresearchgroup.org.uk/images/icons/member-icon.png'
        moderator = 'http://www.clker.com/cliparts/O/f/t/B/a/V/green-hammer-gray.svg.hi.png'
        music = 'http://www.veryicon.com/icon/png/Media/Music%20notes/Note%20green.png'

        # get all the cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and filename not in ignore:
                # get commands from cog
                cog_name = filename[:-3].capitalize()
                cog = self.bot.get_cog(cog_name)
                cog_commands = cog.get_commands()

                # set image for thumbnail
                if cog_name == 'Admin':
                    thumbnail = admin
                elif cog_name == 'Member':
                    thumbnail = member
                elif cog_name == 'Moderator':
                    thumbnail = moderator
                elif cog_name == 'Music':
                    thumbnail = music
                else:
                    thumbnail = ''

                # send an embed for each cog
                eObj = await embed(ctx, title = f'{cog_name} Plugin Commands', thumbnail = thumbnail)   

                # determine command usage
                usage = {
                    # Music
                    'join' : '[member]',
                    'play' : '[search] or [url]',
                    'volume' : '[number]',

                    # Member
                    '_8ball' : '[question]',
                    'echo' : '[string]',

                    # Moderator
                    'clear' : '(optional count)',
                    'kick' : '[member] (optional reason)',
                    'ban' : '[member] (optional reason)',
                    'unban' : '[member] (optional reason)',
                    'warn' : '[member] (optional reason)',
                    'infractions' : '[member]',
                    'clear_infractions' : '[member]',
                    'clear_infraction' : '[infraction id]',
                    'give_bluecan' : '[member]',
                    'remove_bluecan' : '[member]',

                    # Admin
                    'load' : '[extension]',
                    'unload' : '[extension]',
                    'reload' : '[extension]'
                }

                # print all commands and their corresponding descriptions for that cog
                for command in cog_commands:
                    if command.name != 'help' and command.name != '_8ball':
                        usage_string = usage.get(command.name)
                        if not usage_string:
                            usage_string = ''
                        eObj.add_field(name = f'.{command.name} {usage_string}', value = command.description, inline = False)
                    elif command.name == '_8ball':
                        eObj.add_field(name = f'.{command.name[1:]} {usage_string}', value = command.description, inline = False)
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
    async def echo(self, ctx, *, string : str):
        user = ctx.author.display_name
        avatar = ctx.author.avatar_url
        eObj = await embed(ctx, author = user, avatar = avatar, description = string)
        if eObj is not False:
            await ctx.send(embed=eObj)


def setup(bot):
    bot.add_cog(Member(bot))