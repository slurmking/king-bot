#  Copyright (c)Slurmking 2020

import random
import datetime
import logging
from os import listdir

import discord
from discord.ext import commands


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)


currentYear = datetime.date.today().year


def holiday(month, day):
    present = datetime.datetime.now()
    future = datetime.datetime(currentYear, month, day)
    difference = future - present
    return strfdelta(difference, "{days} days {hours} hours and {minutes} minutes")


class Eggs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info(f"\033[92m[COG]\033[0m{self.qualified_name}:loaded")

    async def cog_check(self, ctx):
        if ctx.channel.type == discord.ChannelType.private:
            return False
        else:
            return True

    @commands.command(hidden=True, aliases=['michelle'])
    async def perry(self, ctx):
        image = []
        for file in listdir(f" images/{ctx.invoked_with}"):
            if file.endswith(".jpg"):
                image.append(file)

        await ctx.send(file=discord.File(f' images/{ctx.invoked_with}/{random.choice(image)}'))

    @commands.command(hidden=True)
    async def deletedis(self, ctx):
        await ctx.send(file=discord.File(f' images/etc/deletedis.png'))

    @commands.command(hidden=True)
    async def white(self, ctx):
        await ctx.send(file=discord.File(f' images/etc/white.jpeg'))

    @commands.command(hidden=True)
    async def send(self, ctx):
        file = discord.File(
            "https://scontent-den4-1.cdninstagram.com/v/t50.2886-16/208558944_139571471601351_5092174829592019052_n"
            ".mp4?_nc_ht=scontent-den4-1.cdninstagram.com&_nc_cat=103&_nc_ohc=UkYO67g7T4wAX_Qk13c&edm=APfKNqwBAAAA"
            "&ccb=7-4&oe=60E356E5&oh=bc2c56afbf7039868f1ea8b5576d848c&_nc_sid=74f7ba")
        await ctx.send(file=file, content="Message to be sent")

    @commands.command(hidden=True)
    async def halloween(self, ctx):
        embed = discord.Embed(title="Halloween 🎃")
        embed.set_footer(text=f"Halloween is in {holiday(10, 31)}")
        await ctx.send(embed=embed)

    @commands.command(hidden=True, aliases=['xmas'])
    async def christmas(self, ctx):
        embed = discord.Embed(title="Christmas 🎄")
        embed.set_footer(text=f"Christmas is in {holiday(12, 25)}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Eggs(bot))
