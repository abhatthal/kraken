import sqlite3 # maintain infractions in infractions.db
import logging # maintain logs in bot.log

logging.basicConfig(filename = 'bot.log', level = logging.INFO, format='%(asctime)s %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')

BOT_NAME = 'Honest Bear'
# BOT_AVATAR = 'https://github.com/abhatthal/HonestBear/raw/master/HonestBear.png'
BOT_AVATAR = './images/HonestBear.png'
DESCRIPTION = 'A very honest discord bot'

DATABASE = 'HonestBear.sqlite'
LOGGING_CHANNEL = 607056829067034634

ADMIN_IMG = 'http://icons.iconarchive.com/icons/alecive/flatwoken/512/Apps-Terminal-Pc-104-icon.png'
MEMBER_IMG = 'https://www.airfieldresearchgroup.org.uk/images/icons/member-icon.png'
MODERATOR_IMG = 'http://www.clker.com/cliparts/O/f/t/B/a/V/green-hammer-gray.svg.hi.png'
MUSIC_IMG = 'http://www.veryicon.com/icon/png/Media/Music%20notes/Note%20green.png'