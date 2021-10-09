#  Copyright (c)Slurmking 2020
import discord
from discord.ext import commands
import random
import logging
import json
with open('cogs/dependencies/tarot.json') as f:
    tarotJson = json.load(f)
Major = tarotJson[0]
Cups = tarotJson[1]
Swords = tarotJson[2]
Wands = tarotJson[3]
Pentacles = tarotJson[4]


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
        arcana = [Major, Wands, Swords, Cups, Pentacles]
        deck = (random.choice(arcana))
        coin = random.randint(0, 1)
        card = random.randint(0, len(deck) - 1)
        folder = f"/tarot/{deck[card]['suit']}/"
        modifier = 0
        if deck[card]['suit'] != 'Major':
            modifier = 1
        if coin == 1:
            card_name = (deck[card]['name'])
            card_desc = (deck[card]['meaning'])
            card_loc = f"{folder}{str(int(card) + modifier).zfill(2)}.png"
        else:
            card_name = f"{deck[card]['name']} Reversed"
            card_desc = (deck[card]['reversed'])
            card_loc = f"{folder}{str(int(card + modifier)).zfill(2)}-r.png"

        embed = discord.Embed(colour=7750312)
        embed.set_image(url=f"http://slurmking.com/img/{card_loc}")
        embed.set_author(name=card_name, icon_url=f"http://www.slurmking.com/img/tarot/tarot.png")
        embed.add_field(name="Meaning", value=card_desc)
        print(f"http://slurmking.com/img/{card_loc}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Tarot(bot))
