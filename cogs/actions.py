#  Copyright (c)Slurmking 2020

import configparser
import random
import logging
import aiohttp
import discord
from discord.ext import commands

config = configparser.ConfigParser()
config.read('config.ini')


class Actions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info(f"\033[92m[COG]\033[0m{self.qualified_name}:loaded")

    async def gif(self, ctx, action, verbs, responses):
        random_gen = random.randint(0, 24)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://api.tenor.com/v1/search?q={action}&key={config['api']['tenorkey']}&limit=25")as r:
                if r.status == 200:
                    js = await r.json(content_type='application/json')
                    image = js['results'][random_gen]['media'][0]['mediumgif']['url']
                    embed = discord.Embed(colour=discord.Colour(0xb763a))
                    embed.set_image(url=image)
                    embed.set_author(
                        name=f"{ctx.message.author.name} {random.choice(verbs)} {ctx.message.mentions[0].name}",
                        url='https://discordapp.com', icon_url=f"{ctx.message.author.avatar_url}")
                    embed.set_footer(text=f"{random.choice(responses)}")
                    await ctx.channel.send(embed=embed)

    @commands.command(help="Hug someone", aliases=['cuddle', 'snuggle'])
    async def hug(self, ctx):
        verbs = ['hugs', 'squeezes', 'mushes']
        responses = ['aww', 'so squishy', 'HOW CUTE', 'UwU']
        await self.gif(ctx, 'anime-hug', verbs, responses)

    @commands.command(help="Slap someone")
    async def slap(self, ctx):
        verbs = ['slaps', 'smacks the shit out of', 'smacks']
        responses = ['It\'s on!', 'Oh heck!', 'FIGHT!!!', 'o.o']
        await self.gif(ctx, 'anime-slap', verbs, responses)

    @commands.command(help="Kiss someone")
    async def kiss(self, ctx):
        verbs = ['kisses', 'smooches', 'locks lips with']
        responses = ['I ship it', 'U...UwU??', '🥵', 'Awwww']
        await self.gif(ctx, 'anime-kiss', verbs, responses)

    @commands.command(help="Swoon over someone", aliases=['blush'])
    async def swoon(self, ctx):
        verbs = ['swoons over', 'can\'t get enough of', 'is loving']
        responses = ['I agree', '.....wow']
        await self.gif(ctx, 'anime-blush', verbs, responses)

    @commands.command(help="Think lewd thoughts", aliases=['cry'])
    async def lewd(self, ctx):
        verbs = ['feels lewd about', 'Is having lewd thoughts about', 'think\'s you\'re hot']
        responses = ['🥵', 'Keep it in your pants!!']
        await self.gif(ctx, 'anime-in-love', verbs, responses)

    @commands.command(help="Cry over something")
    async def pout(self, ctx):
        verbs = ['is upset with', 'is pouting at', 'is angwy at']
        responses = ['You better watch out!', 'Aww! It\'s cute when it\'s upset!']
        await self.gif(ctx, 'anime-pout', verbs, responses)

    @commands.command(help="Poke someone", aliases=['boop'])
    async def poke(self, ctx):
        verbs = ['pokes', 'want\'s the attention of', 'boops']
        responses = ['Hey! Listen!', 'HELLO???', 'Good luck']
        await self.gif(ctx, 'anime-poke', verbs, responses)

    @commands.command(hidden=True)
    @commands.is_nsfw()
    async def fuck(self, ctx):
        verbs = ['Fucks', 'Makes love with']
        responses = ['uhhhh......', 'DAMN SON! Where\'d you find this?', 'Good luck']
        await self.gif(ctx, 'anime-makeout', verbs, responses)

    @fuck.error
    async def info_error(self, ctx, error):
        # if isinstance(error, commands.BadArgument):
        await ctx.send(f'{error}')

    @commands.command(help="Pat someone")
    async def pat(self, ctx):
        verbs = ['patts', 'pets']
        responses = ['Pat pat', 'Good boy']
        await self.gif(ctx, 'anime-pat', verbs, responses)

    @commands.command(help="Lick someone")
    async def lick(self, ctx):
        verbs = ['licks', 'tastes', 'defiles']
        responses = ['Tastes like chicken', 'o.....kayy...', 'GET A ROOM!']
        await self.gif(ctx, 'anime-lick', verbs, responses)

    @commands.command(hidden=True)
    async def sploosh(self, ctx):
        embed = discord.Embed(colour=discord.Colour(0xb763a))
        embed.set_image(url="https://media1.tenor.com/images/2fb33d5897dfd3c2c18c214e440af044/tenor.gif")
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Actions(bot))
