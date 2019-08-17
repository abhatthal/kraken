import sqlite3 # maintain infractions in infractions.db
import logging # maintain logs in bot.log

logging.basicConfig(filename = 'bot.log', level = logging.INFO, format='%(asctime)s %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')

BOT_NAME = 'Honest Bear'
BOT_AVATAR = './images/HonestBear.png'
DESCRIPTION = 'A very honest discord bot'
COMMAND_PREFIX = '.'

DATABASE = 'HonestBear.sqlite'
LOGGING_CHANNEL = 607056829067034634

ADMIN_IMG = 'https://raw.githubusercontent.com/abhatthal/HonestBear/master/images/admin.png'
MEMBER_IMG = 'https://raw.githubusercontent.com/abhatthal/HonestBear/master/images/member.png'
MODERATOR_IMG = 'https://raw.githubusercontent.com/abhatthal/HonestBear/master/images/moderator.png'
MUSIC_IMG = 'https://raw.githubusercontent.com/abhatthal/HonestBear/master/images/music.png'
