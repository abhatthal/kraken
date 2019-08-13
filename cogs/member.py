import discord
import random
from discord.ext import commands

class Member(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(brief = 'returns bot latency')
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')
    

    @commands.command(aliases=['8ball'], brief = "Ask a yes or no question, get an answer '8ball [question]'")
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


    @commands.command(brief = 'returns how many members are on the server')
    async def membercount(self, ctx):
        id = self.bot.get_guild(ctx.guild.id)
        await ctx.send(f'Member Count: {id.member_count}')        
        

def setup(bot):
    bot.add_cog(Member(bot))