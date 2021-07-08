#  Copyright (c)Slurmking 2020

import random
import logging
import aiohttp
import discord
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info(f"\033[92m[COG]\033[0m{self.qualified_name}:loaded")

    async def cog_check(self, ctx):
        if ctx.channel.type == discord.ChannelType.private:
            return False
        else:
            return True

    @commands.command(name="8ball", help="Ask the 8ball a question! !8ball am I a pretty girl?", brief='Ask the 8ball')
    async def ball(self, ctx):
        answer = ['It is certain',
                  'It is decidedly so',
                  'Without a doubt',
                  'Yes - definitely',
                  'You may rely on it',
                  'As I see it, yes',
                  'Most likely',
                  'Outlook good',
                  'Yes',
                  'Signs point to yes',
                  'Reply hazy, try again',
                  'Ask again later',
                  'Better not tell you now',
                  'Cannot predict now',
                  'Concentrate and ask again',
                  "don't count on it",
                  'My reply is no',
                  'My sources say no',
                  'Outlook not so good',
                  'Very doubtful']
        await ctx.send(f"🎱{ctx.author.mention} {answer[random.randint(1, len(answer) - 1)]}")

    @commands.command(help="Generates a random pokemon from https://pokemon.alexonsager.net/",
                      brief="Fuse two random pokemon")
    async def pokefusion(self, ctx):
        prefix = ["none", "Bulb", "Ivy", "Venu", "Char", "Char", "Char", "Squirt", "War", "Blast", "Cater", "Meta",
                  "Butter", "Wee", "Kak", "Bee", "Pid", "Pidg", "Pidg", "Rat", "Rat", "Spear", "Fear", "Ek", "Arb",
                  "Pika", "Rai", "Sand", "Sand", "Nido", "Nido", "Nido", "Nido", "Nido", "Nido", "Clef", "Clef", "Vul",
                  "Nin", "Jiggly", "Wiggly", "Zu", "Gol", "Odd", "Gloo", "Vil", "Pa", "Para", "Veno", "Veno", "Dig",
                  "Dug", "Meow", "Per", "Psy", "Gold", "Man", "Prim", "Grow", "Arca", "Poli", "Poli", "Poli", "Ab",
                  "Kada", "Ala", "Ma", "Ma", "Ma", "Bell", "Weepin", "Victree", "Tenta", "Tenta", "Geo",
                  "Grav", "Gol", "Pony", "Rapi", "Slow", "Slow", "Magn", "Magn", "Far", "Do", "Do", "Se", "D", "Gri",
                  "Mu", "Shell", "Cloy", "Gas", "Haunt", "Gen", "On", "Drow", "Hyp", "Krab", "King", "Volt", "Electr",
                  "Exegg", "Exegg", "Cu", "Maro", "Hitmon", "Hitmon", "Licki", "Koff", "We", "Rhy", "Rhy", "Chan",
                  "Tang", "Kangas", "Hors", "Sea", "Gold", "Sea", "Star", "Star", "Mr. ", "Scy", "Jyn", "Electa", "Mag",
                  "Pin", "Tau", "Magi", "Gyara", "Lap", "Dit", "E", "Vapor", "Jolt", "Flar", "Pory", "Oma", "Oma",
                  "Kabu", "Kabu", "Aero", "Snor", "Artic", "Zap", "Molt", "Dra", "Dragon", "Dragon", "Mew", "Mew"]
        suffix = ["none", "basaur", "ysaur", "usaur", "mander", "meleon", "izard", "tle", "tortle", "toise", "pie",
                  "pod", "free", "dle", "una", "drill", "gey", "eotto", "eot", "tata", "icate", "row", "row", "kans",
                  "bok", "chu", "chu", "shrew", "slash", "oran", "rina", "queen", "ran", "rino", "king", "fairy",
                  "fable", "pix", "tales", "puff", "tuff", "bat", "bat", "ish", "oom", "plume", "ras", "sect", "nat",
                  "moth", "lett", "trio", "th", "sian", "duck", "duck", "key", "ape", "lithe", "nine", "wag", "whirl",
                  "wrath", "ra", "bra", "kazam", "chop", "choke", "champ", "sprout", "bell", "bell",
                  "cool", "cruel", "dude", "eler", "em", "ta", "dash", "poke", "bro", "mite", "ton", "fetchd", "duo",
                  "drio", "eel", "gong", "mer", "uk", "der", "ster", "tly", "ter", "gar", "ix", "zee", "no", "by",
                  "ler", "orb", "ode", "cute", "utor", "bone", "wak", "lee", "chan", "tung", "fing", "zing", "horn",
                  "don", "sey", "gela", "khan", "sea", "dra", "deen", "king", "yu", "rmie", "mime", "ther", "nx",
                  "buzz", "mar", "sir", "ros", "karp", "dos", "ras", "to", "vee", "eon", "eon", "eon", "gon", "nyte",
                  "star", "to", "tops", "dactyl", "lax", "cuno", "dos", "tres", "tini ", "nair", "nite", "two", "ew"]
        main = random.randint(1, 151)
        fuse = random.randint(1, 151)
        responses = ["wait... what is that?", "That's not right!", "oh... okay",
                     "Umm....", "Well... it's something", "That's just wrong"]
        random.shuffle(responses)
        img = f"https://images.alexonsager.net/pokemon/fused/{main}/{main}.{fuse}.png"
        url = f"https://pokemon.alexonsager.net/{fuse}/{main}"
        embed = discord.Embed(
            description=responses[0], title=f"{prefix[fuse]}{suffix[main]}", url=url)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.command(help="Get a random cat image")
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.thecatapi.com/v1/images/search') as r:
                if r.status == 200:
                    js = await r.json(content_type='application/json')
                    await ctx.send((js[0]['url']))

    @commands.command(help="Get a random dog image")
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.thedogapi.com/v1/images/search') as r:
                if r.status == 200:
                    js = await r.json(content_type='application/json')
                    await ctx.send((js[0]['url']))


def setup(bot):
    bot.add_cog(Fun(bot))
