#  Copyright (c)Slurmking 2020
import discord
from discord.ext import commands
import random
import logging
import json

with open('bot/cogs/dependencies/tarot.json') as f:
  tarotJson = json.load(f)
Major = tarotJson[0]
Cups = tarotJson[1]
Swords = tarotJson[2]
Wands = tarotJson[3]
Pentacles = tarotJson[4]



def show(number,list):
    if list != Major:
        number = number - 1
        im = Image.open(f"images/tarot/{list[number]['suit']}/{str(number+1).zfill(2)}.png")
        im.show()
    else:
        im = Image.open(f"images/tarot/{list[number]['suit']}/{str(number).zfill(2)}.png")
        im.show()
    return list[number]

class Tarot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info(f"\033[92m[COG]\033[0m{self.qualified_name}:loaded")

    async def cog_check(self, ctx):
        if ctx.channel.type == discord.ChannelType.private:
            return False
        else:
            return True

    @commands.command()
    async def Tarot(self, ctx):
        Arcana = [Major, Wands, Swords, Cups, Pentacles]
        Deck = (random.choice(Arcana))
        Coin = random.randint(0, 1)
        Card = random.randint(0, len(Deck) -1)
        folder = f"/tarot/{Deck[Card]['suit']}/"
        modifier = 0 
        if Deck[Card]['suit'] != 'Major':
            modifier = 1
        if Coin == 1:
            cardName = (Deck[Card]['name'])
            cardDesc = ((Deck[Card]['meaning']))
            cardLoc = (f"{folder}{str(int(Card)+modifier).zfill(2)}.png")
        else:
            cardName = (f"{Deck[Card]['name']} Reversed")
            cardDesc = ((Deck[Card]['reversed']))
            cardLoc = (f"{folder}{str(int(Card+modifier)).zfill(2)}-r.png")

        embed = discord.Embed(colour=7750312)
        embed.set_image(url=f"http://slurmking.com/img/{cardLoc}")
        embed.set_author(name=cardName, icon_url=f"http://www.slurmking.com/img/tarot/tarot.png")
        embed.add_field(name="Meaning",value=cardDesc)
        print(f"http://slurmking.com/img/{cardLoc}")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Tarot(bot))
