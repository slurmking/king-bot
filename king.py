
#  Copyright (c)Slurmking 2020
import configparser
import datetime
import logging
from os import listdir

import discord
from discord.ext import commands

import database

config = configparser.ConfigParser()
config.read('config.ini')
bot = commands.AutoShardedBot(command_prefix=database.get_prefix, case_insensitive=True)

# bot.remove_command('help')
if config['bot']['logging'] == 'True':

    logging.basicConfig(
        filename=f'logs/{datetime.date.today()}.log',
        level=logging.DEBUG, 
        format= '%(asctime)s:%(levelname)s:%(name)s: %(message)s',
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)
@bot.event
async def on_connect():
    database.cache_clear()
    logging.warning('BOT IS STARTING')
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"{config['bot']['status']}"))
    for file in listdir("cogs"):
        if file.endswith(".py"):
            bot.load_extension(f'cogs.{file[:-3]}')
    logging.info('Cogs Loaded')
    logging.info('Creating cache')
    for guild in bot.guilds:
        result = database.load_guild(guild.id)
        try:
            database.cache_update("INSERT OR REPLACE INTO guilds (guild_id, prefix,dj_role)VALUES('%s', '%s','%s');"
                                  % (result['guild_id'], result['prefix'], result['dj_role']))
        except TypeError:
            database.create_guild(guild.id)
    logging.info('Cache created')


@bot.event
async def on_ready():
    logging.info(f'\033[94mStarting {bot.user.display_name} <{bot.user.id}>\033[0m')
    logging.info('\033[96mBot Online\033[0m')
    logging.info(f'\033[96mConnected to\033[0m {len(bot.guilds)} \033[96mservers')


@bot.event
async def on_command(ctx):
    logging.info(
        f'\033[93m[COMMAND]\033[0m{ctx.message.author.name}#{ctx.message.author.discriminator}'
        f':{ctx.message.clean_content}')
# @bot.event
# async def on_message(message):
#     logging.info(
#         f':{message.clean_content}')


@bot.event
async def on_guild_join(guild):
    if database.database_exists('guilds', 'guild_id', str(guild.id)):
        result = database.load_guild(guild.id)
        database.cache_update("INSERT OR REPLACE INTO guilds (guild_id, prefix,dj_role)VALUES('%s', '%s','%s');" % (
            result['guild_id'], '.', result['dj_role']))
    else:
        database.create_guild(guild.id)


#@bot.event
#async def on_command_error(ctx, error):
#    logging.info(
#        f'\033[91m[ERROR]\033[0m{ctx.message.author.name}#{ctx.message.author.discriminator}\'s' \
#        f' {ctx.command} command failed because : {error}')

@bot.event
async def on_shard_connect(shard_id):
    logging.info(
        f'\033[96mshard\033[91m {shard_id}\033[96m started\033[0m')


@bot.listen('on_message')
async def prefixrevert(message):
    if bot.user.mentioned_in(message):
        if 'prefixreset' in message.content:
            if message.author.guild_permissions.administrator:
                await message.channel.send('Prefix reset to [ . ]')
                database.update_guild(message.guild.id, 'prefix', '.')
            else:
                await message.channel.send('You must be an administrator to reset a server\'s prefix')


@bot.command(hidden='true')
@commands.check(commands.guild_only())
async def credits(ctx):
    with open("credits.txt", 'r') as f:
        await ctx.send(f.read())


@bot.command()
@commands.check(commands.guild_only())
async def prefix(ctx, arg):
    if not len(arg) > 1:
        database.update_guild(ctx.guild.id, 'prefix', arg)
        await ctx.send(f'prefix set to [ {arg} ]')
    else:
        await ctx.send('Prefix can only be 1 letter/number long')


@bot.command(hidden='true')
@commands.check(commands.is_owner())
async def status(ctx, *arg):
    config.set('bot', 'status', ' '.join(arg))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=' '.join(arg)))
    with open("config.ini", 'w') as f:
        config.write(f)


@bot.command(hidden='true')
@commands.check(commands.is_owner())
async def reload(ctx, arg):
    bot.reload_extension(f"cogs.{arg}")


@bot.command(hidden='true')
@commands.check(commands.is_owner())
async def loadcog(ctx, arg):
    bot.load_extension(f"cogs.{arg}")


@bot.command(hidden='true')
@commands.check(commands.is_owner())
async def unloadcog(ctx, arg):
    bot.unload_extension(f"cogs.{arg}")


bot.run(config['bot']['key'])
