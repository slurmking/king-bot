#  Copyright (c)Slurmking 2020
import discord
from discord.ext import commands
from random import randint
import logging

class slots:
    def __init__(self):
        self.number = randint(0, 999)

    def spin(self):
        if 0 <= self.number <= 99:
            return 'Queen'
        elif 100 <= self.number <= 399:
            return 'Honey'
        elif 400 <= self.number <= 699:
            return 'Bee1'
        elif 700 <= self.number <= 899:
            return 'Bee2'
        elif 900 <= self.number <= 999:
            return 'Bee3'


def payout(results, bet):
    if results['Queen'] == 3:
        return bet * 200
    elif results['Queen'] == 2:
        return bet * 0
    elif results['Bee3'] == 2:
        return bet * 8
    elif results['Bee3'] == 2:
        return bet * 4
    elif results['Bee2'] == 2:
        return bet * 3
    elif results['Bee1'] == 2:
        return bet * 2
    elif results['Honey'] == 1:
        return bet * 0
    elif results['Honey'] == 2:
        return int(round(bet * 1.5))



    elif results['Honey'] == 3:
        return bet * 2
    elif results['Bee1'] == 3:
        return bet * 4
    elif results['Bee2'] == 3:
        return bet * 6


def slotSpin(bet):
    resultsList = {'Queen': 0,
                   'Bee3': 0,
                   'Bee2': 0,
                   'Bee1': 0,
                   'Honey': 0,
                   }
    reel1 = slots()
    reel2 = slots()
    reel3 = slots()
    resultsList[f"{reel1.spin()}"] += 1
    resultsList[f"{reel2.spin()}"] += 1
    resultsList[f"{reel3.spin()}"] += 1
    logging.info(f"{reel1.spin()} - {reel2.spin()} - {reel3.spin()}")
    logging.info(resultsList)
    if reel2.spin() == reel1.spin():
        if reel2.spin() == reel3.spin():
            output = payout(resultsList, bet)
        else:
            output = payout(resultsList, bet)
    elif resultsList['Honey'] >= 1:
        output = payout(resultsList, bet)
    else:
        output = 0
    return {'results': resultsList,
            'payout': output,
            'reel1': str(reel1.spin()),
            'reel2': str(reel2.spin()),
            'reel3': str(reel3.spin())}


class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info(f"\033[92m[COG]\033[0m{self.qualified_name}:loaded")

    async def cog_check(self, ctx):
        if ctx.channel.type == discord.ChannelType.private:
            return False
        else:
            return True

    @commands.command()
    async def slots(self, ctx, bet=1):
        icons = {'Queen': '<:Queen:862490929599610930>',
                 'Bee1': '<:Bee1:862490929612193822>',
                 'Bee2': '<:Bee2:862490929355816991>',
                 'Bee3': '<:Bee3:862490932065468416>',
                 'Honey': '<:Honey:862490929629757440>',
                 }
        spin = slotSpin(bet)
        # "{reel1} {reel2} {reel3}"
        await ctx.send(f" {icons[spin['reel1']]}{icons[spin['reel2']]} {icons[spin['reel3']]}")
        await ctx.send(f"You got {spin['payout']} [TBD]")


def setup(bot):
    bot.add_cog(games(bot))
