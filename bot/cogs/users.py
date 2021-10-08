#  Copyright (c)Slurmking 2020

import random
import datetime
import logging
from os import listdir

import discord
from discord.ext import commands
from req import database

class users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info(f"\033[92m[COG]\033[0m{self.qualified_name}:loaded")

    async def cog_check(self, ctx):
        if ctx.channel.type == discord.ChannelType.private:
            return False
        else:
            return True

    @commands.command(hidden=True)
    async def register(self, ctx):
        if database.database_exists('Users', 'user_id', str(ctx.author.id)):
            await ctx.send("you already have been registered")
        else:
            database.database_update(f"INSERT INTO `Users` (`user_id`, `level`, `xp`) VALUES ('{ctx.author.id}', '1', '0')")
            await ctx.send("you have been registered")

    @commands.command(hidden=True)
    async def xp(self, ctx):
        if database.database_exists('Users', 'user_id', str(ctx.author.id)):
            xpvalue = database.database_fetch(f"SELECT xp FROM Users WHERE user_id = '{str(ctx.author.id)}'")
            levelvalue = database.database_fetch(f"SELECT level FROM Users WHERE user_id = '{str(ctx.author.id)}'")
            await ctx.send(f"your level is {levelvalue} your xp is {xpvalue}")

    @commands.command(hidden=True)
    async def daily(self, ctx):
        pass

def setup(bot):
    bot.add_cog(users(bot))
