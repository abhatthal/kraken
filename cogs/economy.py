import discord
import random
import sqlite3
from discord.ext import commands
# Shamelessly took helper_files from Wall-E
# https://github.com/CSSS/wall_e/tree/master/helper_files
from helper_files.embed import embed
import helper_files.settings as settings


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description = 'Make yourself a bank account to keep your fish')
    async def make_account(self, ctx):
        # connect to database
        db = sqlite3.connect(settings.DATABASE)
        cursor = db.cursor()
        # check if user already has an account
        cursor.execute(f'SELECT COUNT(*) FROM economy WHERE member_id = {ctx.author.id}')
        account = cursor.fetchone()[0]
        if account >= 1:
            msg = 'You already have an account!'
        else:
            # make an account
            cursor.execute('''
            INSERT INTO economy(member_id, currency)
            VALUES(?, ?)''', (ctx.author.id, 500))
            db.commit()
            msg = "Your account has been registered, here's 500 fish to get you started! <:Asami:610590675142049868>"
        # send user message
        eObj = await embed(ctx, title = 'Honest Bank', author = settings.BOT_NAME,
        avatar = settings.BOT_AVATAR, description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(description = 'Deletes your account and all of your fish')
    async def delete_account(self, ctx):
        # connect to database
        db = sqlite3.connect(settings.DATABASE)
        cursor = db.cursor()
        # delete account
        cursor.execute(f'DELETE FROM economy WHERE member_id = {ctx.author.id}')
        db.commit()
        # send user message
        eObj = await embed(ctx, title = 'Honest Bank', author = settings.BOT_NAME,
        avatar = settings.BOT_AVATAR, description = 'Your account has been deleted.')
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(description = 'see how many fish you have')
    async def check_balance(self, ctx):
        # connect to database
        db = sqlite3.connect(settings.DATABASE)
        cursor = db.cursor()
        # get user account
        cursor.execute(f'SELECT currency FROM economy WHERE member_id = {ctx.author.id}')
        account = cursor.fetchone()
        if str(type(account)) == "<class 'NoneType'>":
            msg = "You don't have an account! Use ``.make_account`` to make one."
        else:
            currency = account[0]
            # return currency
            msg = f'You have {currency} fish. 🐟'
        # send user message
        eObj = await embed(ctx, title = 'Honest Bank', author = settings.BOT_NAME,
        avatar = settings.BOT_AVATAR, description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)
            


def setup(bot):
    bot.add_cog(Economy(bot))