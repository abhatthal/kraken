import sqlite3 # maintain infractions in infractions.db
import logging # maintain logs in bot.log

logging.basicConfig(filename = 'bot.log', level = logging.INFO, format='%(asctime)s %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')

BOT_NAME = 'Honest Bear'
BOT_AVATAR = 'https://github.com/abhatthal/HonestBear/raw/master/HonestBear.png'

# sqlite3 database of all infractions
conn = sqlite3.connect('infractions.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS infractions
            (id text, infraction text, mod_reason text, date text)''')
conn.commit()