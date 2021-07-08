import sqlite3
import datetime


cache = sqlite3.connect('cache.db')
cache_cursor = cache.cursor()


cache_cursor.execute('''INSERT INTO sleep (user_id, channel_id, sleep_time )
VALUES('424s55s','123',datetime('now','localtime'));''')
cache.commit()


# time = '2020-12-23 21:01:24.265486'
# date_time_obj = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
# print(date_time_obj)
#
# if date_time_obj > datetime.datetime.now():
#     print('true')
# else:
#     print('false')

print(datetime.datetime.now())