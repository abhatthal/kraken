import sqlite3 # maintain infractions in infractions.db
import logging # maintain logs in bot.log

logging.basicConfig(filename = 'bot.log', level = logging.INFO, format='%(asctime)s %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')

BOT_NAME = 'Honest Bear'
BOT_AVATAR = 'https://raw.githubusercontent.com/abhatthal/HonestBear/master/images/HonestBear.png'
DESCRIPTION = 'A very honest discord bot'
COMMAND_PREFIX = '.'

DATABASE = 'honestbear.db'

# Thumbnails
ADMIN_IMG = 'https://raw.githubusercontent.com/abhatthal/HonestBear/master/images/admin.png'
ECONOMY_IMG = 'https://raw.githubusercontent.com/abhatthal/HonestBear/master/images/economy.png'
MEMBER_IMG = 'https://raw.githubusercontent.com/abhatthal/HonestBear/master/images/member.png'
MODERATOR_IMG = 'https://raw.githubusercontent.com/abhatthal/HonestBear/master/images/moderator.png'
MUSIC_IMG = 'https://raw.githubusercontent.com/abhatthal/HonestBear/master/images/music.png'

# Channels
LOGGING_CHANNEL = 607056829067034634
DEBATE_CHANNEL = 606880223199363172
SUGGESTIONS_CHANNEL = 607102047195496456
EMOJI_SUGGESTIONS_CHANNEL = 612899402683514880

# Guilds
MAIN_GUILD = 606716567182639105
SUPPORT_GUILD = 608916967579058197

# Custom Emojis
ASAMI_EMOJI = '<:Asami:610219714140045376>'