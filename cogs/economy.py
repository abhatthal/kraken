import discord
import random
from numpy.random import choice # for choosing from a given numerical ditribution
import aiosqlite3
import time # time.time() timestamp
import datetime # datetime.timedelta
import calendar
from discord.ext import commands
from discord.utils import get
# Shamelessly took helper_files from Wall-E
# https://github.com/CSSS/wall_e/tree/master/helper_files
from helper_files.embed import embed
import helper_files.settings as settings
from shutil import copyfile # for backing up database

CURRENCY_NAME = 'fish'
CURRENCY_IMG = '🐟'
BANK_NAME = f'{settings.BOT_NAME} Bank'
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


    @commands.command(aliases = ['50k'], description = f'Check for someone with more than 50k {CURRENCY_NAME}')
    async def _50k(self, ctx):
        try:
            # connect to database
            db = await aiosqlite3.connect(settings.DATABASE)
            cursor = await db.cursor()
            # get first place
            await cursor.execute('SELECT MAX(currency), member_id FROM economy')
            # fetch data
            first = await cursor.fetchone()
            # close connection
            await cursor.close()
            await db.close()
            # get users
            owner = self.bot.get_user(settings.OWNER)
            winner = self.bot.get_user(first[1])
            # send DM
            if (first[0] >= 50000):
                eObj = await embed(ctx, title = 'Economy Winner', description = f'{winner.name} is in first place with {first[0]} {CURRENCY_NAME}!')
                if eObj is not False:
                    await owner.send(embed = eObj)
        except:
            pass


    @commands.command(aliases = ['updateroles'], description = 'manually updates economy roles')
    async def update_roles(self, ctx, member : discord.Member = None):
        if member == None:
            member = ctx.author
        # try block in case roles not in server
        try:
            # Roles
            top10 = get(ctx.guild.roles, id = top10_ID)
            numberone = get(ctx.guild.roles, id = numberone_ID)
            # connect to database
            db = await aiosqlite3.connect(settings.DATABASE)
            cursor = await db.cursor()
            # sort by currency
            await cursor.execute(f'SELECT member_id FROM economy ORDER BY currency DESC')
            # fetch data
            rows = await cursor.fetchall()
            for row in range(len(rows)):
                if rows[row][0] == member.id:
                    rank = row
                    break
            # close connection
            await cursor.close()
            await db.close()
            # update roles
            if rank == 0:
                await member.add_roles(numberone)
            else:
                await member.remove_roles(numberone)
            if rank < 10:
                await member.add_roles(top10)
            else:
                await member.remove_roles(top10)
        except:
            pass
        # check for a winner
        await ctx.invoke(self._50k)
                

    @commands.command(aliases = ['setbalance'], description = "Admins Only: Change a user's balance")
    async def set_balance(self, ctx, amount : int, member : discord.Member = None):
        user_roles = [role.name for role in sorted(ctx.author.roles, key=lambda x: int(x.position), reverse=True)]
        # check member
        run = True
        if member == None:
            member = ctx.author
        if not settings.ADMIN in user_roles:
            run = False
            msg = f"You don't have permission to set balances! {settings.ASAMI_EMOJI}"
        if run:
            # connect to database
            db = await aiosqlite3.connect(settings.DATABASE)
            cursor = await db.cursor()
            # check if user already has an account
            await cursor.execute(f'SELECT COUNT(*) FROM economy WHERE member_id = {member.id}')
            account = await cursor.fetchone()
            account = account[0]
            if account < 1:
                if member == ctx.author:
                    msg = "You don't have an account!"
                else:
                    msg = f"{member.name} doesn't have an account!"
            else:
                # set funds
                await cursor.execute(f'UPDATE economy SET currency = {amount} WHERE member_id = {member.id}')
                await db.commit()
                # close connection
                await cursor.close()
                await db.close()
                if member == ctx.author:
                    msg = f'Your Balance: {amount} {CURRENCY_NAME}'
                else:
                    msg = f"{member.name}'s Balance: {amount} {CURRENCY_NAME}"
            # update roles
            await ctx.invoke(self.update_roles, member)
        # send user message
        eObj = await embed(ctx, title = BANK_NAME, description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(aliases = ['makeaccount'], description = f'Make yourself a bank account to keep your {CURRENCY_NAME}. Admins can add an optional member.')
    async def make_account(self, ctx, member : discord.Member = None):
        user_roles = [role.name for role in sorted(ctx.author.roles, key=lambda x: int(x.position), reverse=True)]
        # check member
        run = True
        if member == None:
            member = ctx.author
        if not settings.ADMIN in user_roles and member != ctx.author:
            run = False
            msg = f"You don't have permission to make bank accounts for others! {settings.ASAMI_EMOJI}"
        if run:
            # connect to database
            db = await aiosqlite3.connect(settings.DATABASE)
            cursor = await db.cursor()
            # check if user already has an account
            await cursor.execute(f'SELECT COUNT(*) FROM economy WHERE member_id = {member.id}')
            account = await cursor.fetchone()
            account = account[0]
            if account >= 1:
                if member == ctx.author:
                    msg = 'You already have an account!'
                else:
                    msg = f'{member.name} already has an account!'
            else:
                # make an account
                await cursor.execute('''
                INSERT INTO economy(member_id, currency)
                VALUES(?, ?)''', (member.id, STARTING_VALUE))
                await db.commit()
                # close connection
                await cursor.close()
                await db.close()
                if member == ctx.author:
                    msg = f"Your account has been registered, here's {STARTING_VALUE} {CURRENCY_NAME} to get you started! {settings.ASAMI_EMOJI}"
                else:
                    msg = f"{member.name}'s account has been registered.\nBalance: {STARTING_VALUE} {CURRENCY_NAME}"
                # update roles
                await ctx.invoke(self.update_roles, member)
        # send user message
        user = member.display_name
        avatar = member.avatar_url
        eObj = await embed(ctx, title = BANK_NAME, author = user,
        avatar = avatar, description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(aliases = ['deleteaccount'], description = f'Admins Only: Deletes an account and all of its {CURRENCY_NAME}')
    async def delete_account(self, ctx, member : discord.Member = None):
        # Roles
        user_roles = [role.name for role in sorted(ctx.author.roles, key=lambda x: int(x.position), reverse=True)]
        top10 = get(ctx.guild.roles, id = top10_ID)
        numberone = get(ctx.guild.roles, id = numberone_ID)
        # check member
        if member == None:
            member = ctx.author
        if settings.ADMIN in user_roles:
            # connect to database
            db = await aiosqlite3.connect(settings.DATABASE)
            cursor = await db.cursor()
            # check if user has an account
            await cursor.execute(f'SELECT COUNT(*) FROM economy WHERE member_id = {member.id}')
            account = await cursor.fetchone()
            account = account[0]
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
                await cursor.execute(f'DELETE FROM economy WHERE member_id = {member.id}')

                await db.commit()
                # close connection
                await cursor.close()
                await db.close()
        else:
            msg = f"You don't have permission to delete bank accounts! {settings.ASAMI_EMOJI}"
        # send user message
        eObj = await embed(ctx, title = BANK_NAME, description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(aliases = ['bal'], description = f'see how many {CURRENCY_NAME} you or someone else have')
    async def balance(self, ctx, member : discord.Member = None):
        # check member
        if member == None:
            member = ctx.author
        # connect to database
        db = await aiosqlite3.connect(settings.DATABASE)
        cursor = await db.cursor()
        # get user account
        await cursor.execute(f'SELECT currency FROM economy WHERE member_id = {member.id}')
        account = await cursor.fetchone()
        if str(type(account)) == "<class 'NoneType'>":
            if member.id == ctx.author.id:
                msg = "You don't have an account! Use ``.make_account`` to make one."
            else:
                msg = f"{member.name} doesn't have an account!"
        else:
            currency = account[0]
            # get rank
            # sort by currency
            await cursor.execute(f'SELECT member_id FROM economy ORDER BY currency DESC')
            # fetch data
            rows = await cursor.fetchall()
            place = 'Not Found'
            for row in range(len(rows)):
                if rows[row][0] == member.id:
                    place = str(row + 1)
            if member.id == ctx.author.id:
                msg = f'You have {currency} {CURRENCY_NAME}. {CURRENCY_IMG}'
            else:
                msg = f'{member.name} has {currency} {CURRENCY_NAME}. {CURRENCY_IMG}'
            msg += '\nRank: ' + place
            # close connection
            await cursor.close()
            await db.close()
            # update roles
            await ctx.invoke(self.update_roles, member)
        # send user message
        user = member.display_name
        avatar = member.avatar_url
        eObj = await embed(ctx, title = BANK_NAME, author = user,
        avatar = avatar, description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)

        
    @commands.command(description = f'give some {CURRENCY_NAME}')
    async def transfer(self, ctx, member : discord.Member, amount : int):
        # connect to database
        db = await aiosqlite3.connect(settings.DATABASE)
        cursor = await db.cursor()
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
                await cursor.execute(f'SELECT currency FROM economy WHERE member_id = {ctx.author.id}')
                account = await cursor.fetchone()
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
                        await cursor.execute(f'SELECT currency FROM economy WHERE member_id = {member.id}')
                        account = await cursor.fetchone()
                        if str(type(account)) == "<class 'NoneType'>":
                            if msg == '':
                                msg = f"{member.name} doesn't have an account!"
                        else:
                            currency_recipient = account[0]
                            # decrease sender account by amount to transfer
                            await cursor.execute(f'UPDATE economy SET currency = {currency_sender - amount} WHERE member_id = {ctx.author.id}')
                            # increase recipient account by amount to transfer
                            await cursor.execute(f'UPDATE economy SET currency = {currency_recipient + amount} WHERE member_id = {member.id}')
                            await db.commit()
                            msg = f"Transfer complete!\nYour Balance: {currency_sender - amount} {CURRENCY_NAME}\n{member.name}'s Balance: {currency_recipient + amount} {CURRENCY_NAME}"
                            # update roles
                            await ctx.invoke(self.update_roles, member)
                            await ctx.invoke(self.update_roles)
        # close connection
        await cursor.close()
        await db.close()
        # send user message
        user = ctx.author.display_name
        avatar = ctx.author.avatar_url
        eObj = await embed(ctx, title = BANK_NAME, author = user,
        avatar = avatar, description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(aliases = ['lb'], description = 'Returns top ten richest toucans')
    async def leaderboard(self, ctx):
        # connect to database
        db = await aiosqlite3.connect(settings.DATABASE)
        cursor = await db.cursor()
        # sort by currency
        await cursor.execute(f'SELECT member_id, currency FROM economy ORDER BY currency DESC')
        # fetch data
        rows = await cursor.fetchall()
        # close connection
        await cursor.close()
        await db.close()
        place = 1
        row_index = 0
        content = []
        while place <= 10 and row_index < len(rows):
            # try in case member wasn't found
            try:
                member = ctx.guild.get_member(rows[row_index][0])
                content.append((f'{place}. {member.name}', f'```{rows[row_index][1]} {CURRENCY_NAME.capitalize()}```'))
                place += 1
            except:
                pass
            row_index += 1
        # send user message
        eObj = await embed(ctx, inline = True, title = f'{CURRENCY_IMG} {BANK_NAME} Leaderboard {CURRENCY_IMG}', content = content)
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(description = 'Free money!')
    async def income(self, ctx):
        msg = ''
        footer = ''
        maintenance = False
        user_roles = [role.name for role in sorted(ctx.author.roles, key=lambda x: int(x.position), reverse=True)]
        if maintenance and not settings.ADMIN in user_roles:
            msg = 'The economy collapsed, we are trying to bail out.'
            footer = 'Command is under maintenance right now!'
        else:
            # connect to database
            db = await aiosqlite3.connect(settings.DATABASE)
            cursor = await db.cursor()
            # check if user has an account
            await cursor.execute(f'SELECT wait_time, currency FROM economy WHERE member_id = {ctx.author.id}')
            account = await cursor.fetchone()
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
                    await cursor.execute(f'UPDATE economy SET currency = {account_value + amount_to_add} WHERE member_id = {ctx.author.id}')
                    # set timer
                    await cursor.execute(f'UPDATE economy SET wait_time = {int(time.time()) + (random.randint(1, 3) * 60 * 60)} WHERE member_id = {ctx.author.id}')
                    await db.commit()
                    msg = f'Success! You gained {amount_to_add} {CURRENCY_NAME}.\nYour Balance: {account_value + amount_to_add} {CURRENCY_NAME}. {CURRENCY_IMG}'
                    footer = 'Come back in a few hours!'
                    # update roles
                    await ctx.invoke(self.update_roles)
            # close connection
            await cursor.close()
            await db.close()
        # send user message
        user = ctx.author.display_name
        avatar = ctx.author.avatar_url
        eObj = await embed(ctx, title = BANK_NAME, description = msg, footer = footer, author = user, avatar = avatar)
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(description = f'Gamble {CURRENCY_NAME} to get {CURRENCY_NAME}, nothing fishy here. >.>')
    async def fish(self, ctx, bet : int):
        msg = ''
        footer = ''
        title = BANK_NAME
        maintenance = False
        user_roles = [role.name for role in sorted(ctx.author.roles, key=lambda x: int(x.position), reverse=True)]
        if maintenance and not settings.ADMIN in user_roles:
            msg = f"Oof, there's no {CURRENCY_NAME} in the pond."
            footer = 'Command is under maintenance right now!'
        else:
            # connect to database
            db = await aiosqlite3.connect(settings.DATABASE)
            cursor = await db.cursor()
            # check if user has an account
            await cursor.execute(f'SELECT currency FROM economy WHERE member_id = {ctx.author.id}')
            account = await cursor.fetchone()
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
                    await cursor.execute(f'UPDATE economy SET currency = {int(account_value + winnings - bet)} WHERE member_id = {ctx.author.id}')
                    await db.commit()
                    msg = f'You bought {bet} {CURRENCY_NAME} worth of bait.\nYou caught {int(winnings)} {CURRENCY_NAME}!\nYour Balance: {int(account_value + winnings - bet)} {CURRENCY_NAME}. {CURRENCY_IMG}'
                    if winnings <= bet:
                        footer = 'Better luck next time!'
                    elif multiplier != multipliers[-1]:
                        footer = 'Congratulations!'
                    else:
                        title = '🎊 GRAND PRIZE WINNER!! 🎊'
                        footer = 'So much fish...'
                # update roles
                await ctx.invoke(self.update_roles)
            # close connection
            await cursor.close()
            await db.close()
        # send user message
        user = ctx.author.display_name
        avatar = ctx.author.avatar_url
        eObj = await embed(ctx, title = title, description = msg, footer = footer, author = user, avatar = avatar)
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(description = "Returns .fish payouts and probabilities")
    async def probability(self, ctx):
        # send user message
        eObj = await embed(ctx, title = f'{BANK_NAME} ``.fish`` Probabilities', footer = f'Code is open-source: https://github.com/abhatthal/{settings.BOT_NAME}')
        # content = []
        for i in range(len(multipliers)):
            eObj.add_field(name = f'{str(multipliers[i])}x', value = f"{str('%.3f'%(weights[i] * 100))}%", inline = True)
            # content.append((f'{str(multipliers[i])}x', f"{str('%.3f'%(weights[i] * 100))}%"))
        if eObj is not False:
            await ctx.send(embed = eObj)


    @commands.command(aliases = ['crasheconomy'], description = "Admins Only: Clears Economy Table")
    async def crash_economy(self, ctx):
        # Roles
        top10 = get(ctx.guild.roles, id = top10_ID)
        numberone = get(ctx.guild.roles, id = numberone_ID)
        user_roles = [role.name for role in sorted(ctx.author.roles, key=lambda x: int(x.position), reverse=True)]

        if settings.ADMIN in user_roles or ctx.author.id == settings.OWNER:
            # connect to database
            db = await aiosqlite3.connect(settings.DATABASE)
            cursor = await db.cursor()
            # get all users in economy
            await cursor.execute('SELECT member_id FROM economy')
            # fetch data
            users = await cursor.fetchall()
            for row_index in range(len(users)):
                # try in case member wasn't found
                try:
                    member = ctx.guild.get_member(users[row_index][0])
                    # delete roles
                    await member.remove_roles(numberone)
                    await member.remove_roles(top10)
                except:
                    pass
            # backup entire database
            copyfile(f'./{settings.DATABASE}', f'../Backups/{calendar.timegm(time.gmtime())}.db')
            # delete all entries in economy table
            await cursor.execute('DELETE FROM economy')
            # close connection
            await cursor.close()
            await db.close()
        else:
            msg = f"You don't have permission to crash the economy! {settings.ASAMI_EMOJI}"
        # send user message
        eObj = await embed(ctx, title = BANK_NAME, description = msg)
        if eObj is not False:
            await ctx.send(embed = eObj)


    async def cog_check(self, ctx):
        user_roles = [role.name for role in sorted(ctx.author.roles, key=lambda x: int(x.position), reverse=True)]
        return settings.MODERATOR in user_roles or settings.ADMIN in user_roles or ctx.author.id == settings.OWNER or ctx.channel.id in (settings.BOT_SPAM_CHANNEL, settings.ECONOMY_CHANNEL)


def setup(bot):
    bot.add_cog(Economy(bot))