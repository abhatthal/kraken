import sqlite3 # maintain infractions in infractions.db
import logging # maintain logs in bot.log
import json # to read blacklist

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
## General
DEBATE_CHANNEL = 606880223199363172
WEEB_CHANNEL = 613162960642113602
MAGAUS_CHANNEL = 606917477192040460
COOKING_CHANNEL = 639649441904853002
SUGGESTIONS_CHANNEL = 607102047195496456
EMOJI_SUGGESTIONS_CHANNEL = 612899402683514880
ART_CHANNEL = 607021491271368803
FANART_CHANNEL = 608062436335026199
PROPER_CHANNEL = 606912060231778320
## Moderators
LOGGING_CHANNEL = 607056829067034634
## Shitposting
RETARDVILLE_CHANNEL = 606889975908270110
MEMES_CHANNEL = 606929708440879154
## Botting
MUSIC_CHANNEL = 625594220505202698
BOT_SPAM_CHANNEL = 606920734693916674
ECONOMY_CHANNEL = 612898538447306752
## Bluecans (VC)
GENERAL_VC_CHANNEL = 638238393704251392

# Custom Emojis
ASAMI_EMOJI = '<:Asami:610219714140045376>'
KASH_DAB_EMOJI = '<:kash_dab:620410299933261844>'

# Roles
MODERATOR = 'mod'
ADMIN = 'GOD'

# Blacklist
with open('blacklist.json', 'r') as f:
    BLACKLIST = json.load(f)
    f.close()