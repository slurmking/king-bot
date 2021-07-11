#  Copyright (c)Slurmking 2020

import configparser
import sqlite3

import mysql.connector

config = configparser.ConfigParser()
config.read('setup/config.ini')
mydb = mysql.connector.connect(
    host=f"{config['mysql']['host']}",
    user=f"{config['mysql']['user']}",
    port=f"{config['mysql']['port']}",
    password=f"{config['mysql']['password']}",
    database=f"{config['mysql']['database']}"
)
cache = sqlite3.connect('setup/cache.db')
cache_cursor = cache.cursor()
mycursor = mydb.cursor()


def load_guild(guild_id):
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(f"SELECT * FROM `guilds` WHERE `guild_id` = {guild_id}")
    guild = mycursor.fetchone()
    mydb.commit()
    return guild


def database_update(arg):
    mycursor.execute(arg)
    mydb.commit()


def cache_update(arg):
    cache_cursor.execute(arg)
    cache.commit()


def database_exists(table, column, value):
    mycursor.execute("""SELECT EXISTS(SELECT * FROM %s WHERE %s = %s)""" % (table, column, value))
    value = mycursor.fetchone()
    if value:
        if value[0] == 0:
            return False
        elif value[0] == 1:
            return True
    else:
        return None
    mydb.commit()


def cache_exists(table, column, value):
    mycursor.execute("""SELECT EXISTS(SELECT * FROM %s WHERE %s = %s)""" % (table, column, value))
    value = cache_cursor.fetchone()
    if value:
        if value[0] == 0:
            return False
        elif value[0] == 1:
            return True
    else:
        return None
    cache.commit()


def cache_dj(guild_id):
    cache_cursor.execute("""SELECT dj_role FROM guilds WHERE guild_id = '%s'""" % guild_id)
    value = cache_cursor.fetchone()
    if value:
        if value[0] is None:
            return None
        else:
            return value[0]
    else:
        return None
    cache.commit()


def cache_clear():
    cache_update("""DROP TABLE IF EXISTS guilds;""")
    cache_update("""CREATE TABLE "guilds" (
    "guild_id"	TEXT NOT NULL UNIQUE,
    "prefix"	TEXT DEFAULT '.',
    "dj_role"	TEXT DEFAULT 'None')""")


def get_prefix(bot, message):
    try:
        cache_update(f"SELECT prefix FROM guilds WHERE guild_id = '{message.guild.id}'")
        result = cache_cursor.fetchone()
    except:
        pass
    if result:
        return result[0]
    else:
        return '.'


def update_guild(guild_id, row, value):
    cache_update("""UPDATE guilds SET %s = '%s' WHERE guild_id='%s'""" % (row, value, guild_id))
    database_update("""UPDATE `guilds` SET `%s` = '%s' WHERE `guilds`.`guild_id` = %s""" % (row, value, guild_id))


def create_guild(guild_id):
    database.cache_update("""INSERT INTO "main"."guilds"("guild_id") VALUES ('%s');""" % guild_id)
    database.database_update(
        """INSERT INTO `guilds` (`guild_id`, `prefix`, `dj_role`) VALUES ('%s', '.', NULL);""" % guild_id)
