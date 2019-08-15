import discord
import random
from discord.ext import commands
# Shamelessly took helper_files from Wall-E
# https://github.com/CSSS/wall_e/tree/master/helper_files
from helper_files.embed import embed
import helper_files.settings as settings


class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context = True, description = 'under construction')
    async def help2(self, ctx):
        user = ctx.author.display_name
        avatar = ctx.author.avatar_url

        eObj = await embed(ctx, title = f'{settings.BOT_NAME} - Help', description = settings.DESCRIPTION)
        eObj.add_field(name = 'ping', value = 'returns bot latency', inline = False)
        eObj.add_field(name = '8ball', value = "Ask a yes or no question, get an answer '8ball [question]'", inline = False)
        if eObj is not False:
            await ctx.send(embed = eObj)

        msg = '```'
        for command in self.bot.commands:
            msg += f'{command.category} - {command.name} - {command.description}\n'
        msg += '```'
        await ctx.send(msg)


    @commands.command(description = 'returns bot latency')
    async def ping(self, ctx):
        eObj = await embed(ctx, description = f'Pong! {round(self.bot.latency * 1000)}ms', author = settings.BOT_NAME, avatar = settings.BOT_AVATAR)
        if eObj is not False:
            await ctx.send(embed = eObj)
    

    @commands.command(aliases=['8ball'], description = "Ask a yes or no question, get an answer '8ball [question]'")
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