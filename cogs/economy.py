import discord
import random
import sqlite3
from discord.ext import commands
# Shamelessly took helper_files from Wall-E
# https://github.com/CSSS/wall_e/tree/master/helper_files
from helper_files.embed import embed
import helper_files.settings as settings

CURRENCY_NAME = 'fish'
CURRENCY_IMG = '🐟'

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description = f'Make yourself a bank account to keep your {CURRENCY_NAME}')
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
            msg = f"Your account has been registered, here's 500 {CURRENCY_NAME} to get you started! <:Asami:610590675142049868>"
        # send user message
        eObj = await embed(ctx, title = 'Honest Bank', author = settings.BOT_NAME,
        avatar = settings.BOT_AVATAR, description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)


    # For testing purposes
    '''
    @commands.command(description = f'Deletes your account and all of your {CURRENCY_NAME}')
    async def delete_account(self, ctx):
        # connect to database
        db = sqlite3.connect(settings.DATABASE)
        cursor = db.cursor()
        # check if user has an account
        cursor.execute(f'SELECT COUNT(*) FROM economy WHERE member_id = {ctx.author.id}')
        account = cursor.fetchone()[0]
        if account < 1:
            msg = "You don't have an account!"
        else:
            msg = 'Your account has been deleted.'
            # delete account
            cursor.execute(f'DELETE FROM economy WHERE member_id = {ctx.author.id}')
            db.commit()
        # send user message
        eObj = await embed(ctx, title = 'Honest Bank', author = settings.BOT_NAME,
        avatar = settings.BOT_AVATAR, description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)
    '''


    @commands.command(description = f'see how many {CURRENCY_NAME} you or someone else have')
    async def check_balance(self, ctx, member : discord.Member = None):
        # check member
        if member == None:
            member = ctx.author
        # connect to database
        db = sqlite3.connect(settings.DATABASE)
        cursor = db.cursor()
        # get user account
        cursor.execute(f'SELECT currency FROM economy WHERE member_id = {member.id}')
        account = cursor.fetchone()
        if str(type(account)) == "<class 'NoneType'>":
            if member.id == ctx.author.id:
                msg = "You don't have an account! Use ``.make_account`` to make one."
            else:
                msg = f"{member.name} doesn't have an account!"
        else:
            currency = account[0]
            if member.id == ctx.author.id:
                msg = f'You have {currency} {CURRENCY_NAME}. {CURRENCY_IMG}'
            else:
                msg = f'{member.name} has {currency} {CURRENCY_NAME}. {CURRENCY_IMG}'
        # send user message
        eObj = await embed(ctx, title = 'Honest Bank', author = settings.BOT_NAME,
        avatar = settings.BOT_AVATAR, description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)

        
    @commands.command(description = f'give some {CURRENCY_NAME}')
    async def transfer(self, ctx, member : discord.Member, amount : int):
        # connect to database
        db = sqlite3.connect(settings.DATABASE)
        cursor = db.cursor()
        msg = ''
        # check if amount is valid
        if amount <= 0:
            msg = 'Amount transferred must be > 0'
        else:
            # check if member is valid
            if member.id == ctx.author.id:
                msg = "You can't transfer funds to yourself"
            else:
                # get sender account
                cursor.execute(f'SELECT currency FROM economy WHERE member_id = {ctx.author.id}')
                account = cursor.fetchone()
                if str(type(account)) == "<class 'NoneType'>":
                    if msg == '':
                        msg = "You don't have an account! Use ``.make_account`` to make one"
                else:
                    currency_sender = account[0]
                    if amount > currency_sender:
                        if msg == '':
                            msg = 'You have insufficient funds!'
                    else:
                        # get recipient account
                        cursor.execute(f'SELECT currency FROM economy WHERE member_id = {member.id}')
                        account = cursor.fetchone()
                        if str(type(account)) == "<class 'NoneType'>":
                            if msg == '':
                                msg = f"{member.name} doesn't have an account!"
                        else:
                            currency_recipient = account[0]
                            # decrease sender account by amount to transfer
                            cursor.execute(f'UPDATE economy SET currency = {currency_sender - amount} WHERE member_id = {ctx.author.id}')
                            # increase recipient account by amount to transfer
                            cursor.execute(f'UPDATE economy SET currency = {currency_recipient + amount} WHERE member_id = {member.id}')
                            db.commit()
                            msg = f"Transfer complete!\nYour Balance: {currency_sender - amount} {CURRENCY_NAME}\n{member.name}'s Balance: {currency_recipient + amount} {CURRENCY_NAME}"
        # send user message
        eObj = await embed(ctx, title = 'Honest Bank', author = settings.BOT_NAME,
        avatar = settings.BOT_AVATAR, description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(description = 'Returns top ten richest toucans')
    async def leaderboard(self, ctx):
        # connect to database
        db = sqlite3.connect(settings.DATABASE)
        cursor = db.cursor()
        # sort by currency
        cursor.execute(f'SELECT member_id, currency FROM economy ORDER BY currency DESC')
        # fetch data
        rows = cursor.fetchall()
        place = 1
        row_index = 0
        # top 10
        eObj = await embed(ctx, title = f'{CURRENCY_IMG} Honest Bank Leaderboard {CURRENCY_IMG}')
        while place <= 10 and row_index < len(rows):
            # try in case member wasn't found
            try:
                member = ctx.guild.get_member(rows[row_index][0])
                eObj.add_field(name = f'{place}. {member.name}#{member.discriminator}', value = f'```{rows[row_index][1]} {CURRENCY_NAME.capitalize()}```', inline = False)
                place += 1
            except:
                pass
            row_index += 1
        # send user message
        if eObj is not False:
            await ctx.send(embed = eObj)
            

def setup(bot):
    bot.add_cog(Economy(bot))