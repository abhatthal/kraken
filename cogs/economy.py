import discord
import random
from numpy.random import choice # for choosing from a given numerical ditribution
import sqlite3
import asyncio # await asyncio.sleep()
import time # time.time() timestamp
import datetime # datetime.timedelta
from discord.ext import commands
from discord.utils import get
# Shamelessly took helper_files from Wall-E
# https://github.com/CSSS/wall_e/tree/master/helper_files
from helper_files.embed import embed
import helper_files.settings as settings

CURRENCY_NAME = 'fish'
CURRENCY_IMG = '🐟'
STARTING_VALUE = 500

# payouts for .fish
multipliers = [0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 1, 2, 3, 4, 5, 10, 100, 1000]
weights = [0.7 / 8, 0.7 / 8, 0.7 / 8, 0.7 / 8, 0.7 / 8, 0.7 / 8, 0.7 / 8, 0.7 / 8, 0.29889 / 5, 0.29889 / 5, 0.29889 / 5, 0.29889 / 5, 0.29889 / 5, 0.001, 0.0001, 0.00001]

# Role to give to top 10 users
top10_ID = 613578438707511326
numberone_ID = 613598305263288334


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description = "manually updates economy roles")
    async def update_roles(self, ctx, member : discord.Member = None):
        if member == None:
            member = ctx.author
        # Roles 
        top10 = get(ctx.guild.roles, id = top10_ID)
        numberone = get(ctx.guild.roles, id = numberone_ID)
        # connect to database
        db = sqlite3.connect(settings.DATABASE)
        cursor = db.cursor()
        # sort by currency
        cursor.execute(f'SELECT member_id FROM economy ORDER BY currency DESC')
        # fetch data
        rows = cursor.fetchall()
        for row in range(len(rows)):
            if rows[row][0] == member.id:
                rank = row
                break
        # await ctx.send(rank)
        # update roles
        if rank == 0:
            await member.add_roles(numberone)
        else:
            await member.remove_roles(numberone)
        if rank <= 10:
            await member.add_roles(top10)
        else:
            await member.remove_roles(top10)
                

    @commands.command(description = "Admins Only: Change a user's balance")
    @commands.has_role('GOD')
    async def set_balance(self, ctx, amount : int, member : discord.Member = None):
        # check member
        if member == None:
            member = ctx.author
        # connect to database
        db = sqlite3.connect(settings.DATABASE)
        cursor = db.cursor()
        # check if user already has an account
        cursor.execute(f'SELECT COUNT(*) FROM economy WHERE member_id = {member.id}')
        account = cursor.fetchone()[0]
        if account < 1:
            if member == ctx.author:
                msg = "You don't have an account!"
            else:
                msg = f"{member.name} doesn't have an account!"
        else:
            # set funds
            cursor.execute(f'UPDATE economy SET currency = {amount} WHERE member_id = {member.id}')
            db.commit()
            if member == ctx.author:
                msg = f'Your Balance: {amount} {CURRENCY_NAME}'
            else:
                msg = f"{member.name}'s Balance: {amount} {CURRENCY_NAME}"
        # update roles
        await ctx.invoke(self.update_roles, member)
        # send user message
        eObj = await embed(ctx, title = 'Honest Bank', description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(description = f'Make yourself a bank account to keep your {CURRENCY_NAME}. Admins can add an optional member.')
    async def make_account(self, ctx, member : discord.Member = None):
        # check member
        run = True
        if member == None:
            member = ctx.author
        elif not ('GOD' in [role.name for role in ctx.author.roles]):
            run = False
            msg = f"You don't have permission to make bank accounts for others! {settings.ASAMI_EMOJI}"
        if run:
            # connect to database
            db = sqlite3.connect(settings.DATABASE)
            cursor = db.cursor()
            # check if user already has an account
            cursor.execute(f'SELECT COUNT(*) FROM economy WHERE member_id = {member.id}')
            account = cursor.fetchone()[0]
            if account >= 1:
                if member == ctx.author:
                    msg = 'You already have an account!'
                else:
                    msg = f'{member.name} already has an account!'
            else:
                # make an account
                cursor.execute('''
                INSERT INTO economy(member_id, currency)
                VALUES(?, ?)''', (member.id, STARTING_VALUE))
                db.commit()
                if member == ctx.author:
                    msg = f"Your account has been registered, here's {STARTING_VALUE} {CURRENCY_NAME} to get you started! {settings.ASAMI_EMOJI}"
                else:
                    msg = f"{member.name}'s account has been registered.\nBalance: {STARTING_VALUE} {CURRENCY_NAME}"
                # update roles
                await ctx.invoke(self.update_roles, member)
        # send user message
        eObj = await embed(ctx, title = 'Honest Bank', description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(description = f'Admins Only: Deletes an account and all of its {CURRENCY_NAME}')
    async def delete_account(self, ctx, member : discord.Member = None):
        # Roles 
        top10 = get(ctx.guild.roles, id = top10_ID)
        numberone = get(ctx.guild.roles, id = numberone_ID)
        # check member
        if member == None:
            member = ctx.author
        if 'GOD' in [role.name for role in ctx.author.roles]:
            # connect to database
            db = sqlite3.connect(settings.DATABASE)
            cursor = db.cursor()
            # check if user has an account
            cursor.execute(f'SELECT COUNT(*) FROM economy WHERE member_id = {member.id}')
            account = cursor.fetchone()[0]
            if account < 1:
                if member == ctx.author:
                    msg = "You don't have an account! Use ``.make_account`` to make one."
                else:
                    msg = f"{member.name} doesn't have an account!"
            else:
                if member == ctx.author:
                    msg = 'Your account has been deleted.'
                else:
                    msg = f"{member.name}'s account has been deleted."
                # delete roles
                await member.remove_roles(numberone)
                await member.remove_roles(top10)
                # delete account
                cursor.execute(f'DELETE FROM economy WHERE member_id = {member.id}')
                db.commit()
        else:
            msg = f"You don't have permission to delete bank accounts! {settings.ASAMI_EMOJI}"
        # send user message
        eObj = await embed(ctx, title = 'Honest Bank', description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)


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
            # get rank
            # sort by currency
            cursor.execute(f'SELECT member_id FROM economy ORDER BY currency DESC')
            # fetch data
            rows = cursor.fetchall()
            place = 'Not Found'
            for row in range(len(rows)):
                if rows[row][0] == member.id:
                    place = str(row + 1)
            if member.id == ctx.author.id:
                msg = f'You have {currency} {CURRENCY_NAME}. {CURRENCY_IMG}'
            else:
                msg = f'{member.name} has {currency} {CURRENCY_NAME}. {CURRENCY_IMG}'
            msg += '\nRank: ' + place
            # update roles
            await ctx.invoke(self.update_roles, member)
        # send user message
        user = member.display_name
        avatar = member.avatar_url
        eObj = await embed(ctx, title = 'Honest Bank', author = user,
        avatar = avatar, description = msg)
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
                            # update roles
                            await ctx.invoke(self.update_roles, member)
                            await ctx.invoke(self.update_roles)
        # send user message
        eObj = await embed(ctx, title = 'Honest Bank', description = msg)
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
                eObj.add_field(name = f'{place}. {member.name}', value = f'```{rows[row_index][1]} {CURRENCY_NAME.capitalize()}```', inline = True)
                place += 1
            except:
                pass
            row_index += 1
        # send user message
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(description = 'Free money!')
    async def income(self, ctx):
        msg = ''
        footer = ''
        maintenance = False
        if maintenance and not ('GOD' in [role.name for role in ctx.author.roles]):
            msg = 'The economy collapsed, we are trying to bail out.'
            footer = 'Command is under maintenance right now!'
        else:
            # connect to database
            db = sqlite3.connect(settings.DATABASE)
            cursor = db.cursor()
            # check if user has an account
            cursor.execute(f'SELECT wait_time, currency FROM economy WHERE member_id = {ctx.author.id}')
            account = cursor.fetchone()
            if type(account) != tuple:
                msg = "You don't have an account! Use ``.make_account`` to make one"
            else:
                # check if user can use this command
                wait = account[0]
                if wait == None:
                    wait = 0
                time_left = wait - int(time.time())
                if time_left > 0:
                    msg = 'Sorry! Come back later.'
                    footer = f'Time Left: {str(datetime.timedelta(seconds = time_left))}'
                else:
                    # add money to account
                    account_value = account[1]
                    base = int(STARTING_VALUE / 50)
                    amount_to_add = random.randrange(base, (10 * base) + 1, base)
                    cursor.execute(f'UPDATE economy SET currency = {account_value + amount_to_add} WHERE member_id = {ctx.author.id}')
                    # set timer
                    cursor.execute(f'UPDATE economy SET wait_time = {int(time.time()) + (random.randint(1, 3) * 60 * 60)} WHERE member_id = {ctx.author.id}')
                    db.commit()
                    msg = f'Success! You gained {amount_to_add} {CURRENCY_NAME}.\nYour Balance: {account_value + amount_to_add} {CURRENCY_NAME}. {CURRENCY_IMG}'
                    footer = 'Come back in a few hours!'
                await ctx.invoke(self.update_roles)
        # send user message
        user = ctx.author.display_name
        avatar = ctx.author.avatar_url
        eObj = await embed(ctx, title = 'Honest Bank', description = msg, footer = footer, author = user, avatar = avatar)
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(description = f'Gamble {CURRENCY_NAME} to get {CURRENCY_NAME}, nothing fishy here. >.>')
    async def fish(self, ctx, bet : int):
        msg = ''
        footer = ''
        title = 'Honest Bank'
        maintenance = False
        if maintenance and not ('GOD' in [role.name for role in ctx.author.roles]):
            msg = f"Oof, there's no {CURRENCY_NAME} in the pond."
            footer = 'Command is under maintenance right now!'
        else:
            # connect to database
            db = sqlite3.connect(settings.DATABASE)
            cursor = db.cursor()
            # check if user has an account
            cursor.execute(f'SELECT currency FROM economy WHERE member_id = {ctx.author.id}')
            account = cursor.fetchone()
            if type(account) != tuple:
                msg = "You don't have an account! Use ``.make_account`` to make one"
            else:
                # check if amount is valid
                account_value = account[0]
                if bet <= 0:
                    msg = f'Bet invalid, please bet a positive integer amount of {CURRENCY_NAME}'
                elif bet > account_value:
                    msg = f"You don't have that much {CURRENCY_NAME} to bet!"
                else:
                    # update account
                    multiplier = choice(multipliers, p = weights)
                    winnings = bet * multiplier
                    cursor.execute(f'UPDATE economy SET currency = {int(account_value + winnings - bet)} WHERE member_id = {ctx.author.id}')
                    db.commit()
                    msg = f'You won {int(winnings)} {CURRENCY_NAME}!\nYour Balance: {int(account_value + winnings - bet)} {CURRENCY_NAME}. {CURRENCY_IMG}'
                    if winnings <= bet:
                        footer = 'Better luck next time!'
                    elif multiplier != multipliers[-1]:
                        footer = 'Congratulations!'
                    else:
                        title = '🎊 GRAND PRIZE WINNER!! 🎊'
                        footer = 'So much fish...'
                # update roles
                await ctx.invoke(self.update_roles)
        # send user message
        user = ctx.author.display_name
        avatar = ctx.author.avatar_url
        eObj = await embed(ctx, title = title, description = msg, footer = footer, author = user, avatar = avatar)
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(description = "Returns .fish payouts and probabilities")
    async def probability(self, ctx):
        # send user message
        eObj = await embed(ctx, title = 'Honest Bank ``.fish`` Probabilities', footer = 'Code is open-source: https://github.com/abhatthal/HonestBear')
        for i in range(len(multipliers)):
            eObj.add_field(name = f'{str(multipliers[i])}x', value = f"{str('%.3f'%(weights[i] * 100))}%", inline = True)
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(description = "Find the poorest toucan")
    async def who_is_poorest(self, ctx):
        # connect to database
        db = sqlite3.connect(settings.DATABASE)
        cursor = db.cursor()
        # get poorest user
        cursor.execute(f'SELECT member_id FROM economy ORDER BY currency ASC')
        member = ctx.guild.get_member(cursor.fetchone()[0])
        user = member.display_name
        avatar = member.avatar_url
        # send user message
        msg = f"Haha, {member.name}#{member.discriminator} is the poorest toucan.\nLet's all point and laugh. ☝"
        eObj = await embed(ctx, title = 'Honest Bank', description = msg, footer = 'Hahaha... ', author = user, avatar = avatar)
        if eObj is not False:
            await ctx.send(embed = eObj)


def setup(bot):
    bot.add_cog(Economy(bot))