import sqlite3 # maintain infractions in infractions.db
import logging # maintain logs in bot.log
import json # to read blacklist

logging.basicConfig(filename = 'bot.log', level = logging.INFO, format='%(asctime)s %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')

BOT_NAME = 'Kraken'
BOT_AVATAR = 'https://raw.githubusercontent.com/abhatthal/Kraken/master/images/Kraken.png'
DESCRIPTION = 'Part-time legendary sea monster, full-time Discord bot.'
COMMAND_PREFIX = '.'

DATABASE = 'kraken.db'

# Thumbnails
ADMIN_IMG = 'https://raw.githubusercontent.com/abhatthal/Kraken/master/images/admin.png'
ECONOMY_IMG = 'https://raw.githubusercontent.com/abhatthal/Kraken/master/images/economy.png'
MEMBER_IMG = 'https://raw.githubusercontent.com/abhatthal/Kraken/master/images/member.png'
MODERATOR_IMG = 'https://raw.githubusercontent.com/abhatthal/Kraken/master/images/moderator.png'
MUSIC_IMG = 'https://raw.githubusercontent.com/abhatthal/Kraken/master/images/music.png'

# Channels
## General
COOKING_CHANNEL = 639649441904853002
WEEB_CHANNEL = 613162960642113602
ART_CHANNEL = 607021491271368803
VIDEO_SUGGESTIONS_CHANNEL = 696834226313625641
SERVER_SUGGESTIONS_CHANNEL = 607102047195496456
EMOJI_SUGGESTIONS_CHANNEL = 612899402683514880
PROPER_CHANNEL = 606912060231778320
## Gaming
GAMING_CHANNEL = 625511819938758667
## Moderators
LOGGING_CHANNEL = 607056829067034634
## Bots
MUSIC_CHANNEL = 625594220505202698
BOT_SPAM_CHANNEL = 606920734693916674
ECONOMY_CHANNEL = 612898538447306752

# Custom Emojis
ASAMI_EMOJI = '<:Asami:610219714140045376>'
KASH_DAB_EMOJI = '<:kash_dab:620410299933261844>'

# Roles
MODERATOR = 'mod'
OWNER = 330178605936017408
BOT_MANAGER = 722573533707763762

# Disabled Cogs
DISABLED_COGS = ['music.py']

# Blacklist
with open('blacklist.json', 'r') as f:
    BLACKLIST = json.load(f)
    f.close()
