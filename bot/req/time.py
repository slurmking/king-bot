import sqlite3
import datetime
import logging

cache = sqlite3.connect('setup/cache.db')
cache_cursor = cache.cursor()


cache_cursor.execute('''INSERT INTO sleep (user_id, channel_id, sleep_time )
VALUES('424s55s','123',datetime('now','localtime'));''')
cache.commit()

