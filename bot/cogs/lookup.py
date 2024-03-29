#  Copyright (c)Slurmking 2020

import aiohttp
import discord
from discord.ext import commands
import logging


class Lookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info(f"\033[92m[COG]\033[0m{self.qualified_name}:loaded")

    @staticmethod
    def mc_escape(string):
        string = list(string)
        for _ in range(3):
            for index, x in enumerate(string):
                if x == '§' or x == '\n':
                    del string[index:index + 2]
        return ''.join(string)

    async def cog_check(self, ctx):
        if ctx.channel.type == discord.ChannelType.private:
            return False
        else:
            return True

    @commands.command(help="Gets info from IMDB")
    @commands.check(commands.guild_only())
    async def imdb(self, ctx, *args):
        argument = '+'.join(args[:])
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.omdbapi.com/?t=' + str(argument) + '&apikey=1fe03f58') as r:
                if r.status == 200:
                    response = await r.json(content_type='application/json')
        embed = discord.Embed(title=response['Title'], color=0xff6027,
                              url=f"https://www.imdb.com/title/{response['imdbID']}")
        embed.set_thumbnail(url=response['Poster'])
        embed.add_field(name='Rated', value=response['Rated'])
        embed.add_field(name='Released', value=response['Year'])
        embed.add_field(name='Runtime', value=response['Runtime'])
        embed.add_field(name='Genre', value=response['Genre'])
        await ctx.send(embed=embed)

    @commands.command(help="Defines a word with Urban Dictionary")
    async def urban(self, ctx, *args):
        argument = ''.join(args[:])
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.urbandictionary.com/v0/define?term=' + str(argument))as r:
                if r.status == 200:
                    response = await r.json(content_type='application/json')
        embed = discord.Embed(
            description=response['list'][0]['definition'], color=0xff6027)
        embed.set_thumbnail(
            url='https://d2gatte9o95jao.cloudfront.net/assets/apple-touch-icon'
                '-1734beeaa059fbc5587bddb3001a0963670c6de8767afb6c67d88d856b0c0dad.png')
        embed.add_field(name='Example', value=response['list'][0]['example'])
        embed.set_author(name=response['list'][0]['word'],
                         url=response['list'][0]['permalink'])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Lookup(bot))
