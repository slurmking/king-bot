#  Copyright (c)Slurmking 2020
import discord
from discord.ext import commands
import ctypes
from bot.req import econ
import logging
from bot.req import database
from bot.cogs.dependencies import slots
from bot.cogs.dependencies import blackjack


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
        if bet > 500:
            await ctx.send(f"Bet must be under 500")
            return
        wallet = econ.lookup(ctx.message.author.id)
        try:
            econ.update(ctx.message.author.id, bet * -1)
        except econ.currency_mismatch:
            await ctx.send(f"Not enough money")
            return
        icons = {'Queen': '<:Queen:862490929599610930>',
                 'Bee1': '<:Bee1:862490929612193822>',
                 'Bee2': '<:Bee2:862490929355816991>',
                 'Bee3': '<:Bee3:862490932065468416>',
                 'Honey': '<:Honey:862490929629757440>',
                 }
        spin = slots.slot_spin(bet)
        payout = spin['payout']
        # "{reel1} {reel2} {reel3}"
        econ.update(ctx.message.author.id, payout)
        await ctx.send(f" {icons[spin['reel1']]}{icons[spin['reel2']]} {icons[spin['reel3']]}")
        await ctx.send(f"You got {spin['payout']} Gold\n you have {econ.format(econ.lookup(ctx.message.author.id))} Gold")

    @commands.command()
    async def blackjack(self,ctx):
        print(blackjack.gamelist)
        if f'{ctx.author.id}' in blackjack.gamelist:
            game = blackjack.gamelist[f'{ctx.author.id}']
            await ctx.send(f"{id(game)}")
            return
        else:
            blackjack.gamelist[f'{ctx.author.id}'] = blackjack.game(5,f'{ctx.author.id}')
            game = blackjack.gamelist[f'{ctx.author.id}']
            game.start()
            await ctx.send(f"{id(game)}")
            await ctx.send(f"{game.dealer_hand},{game.player_hand}\n"
                           f"{game.dealer_score,game.player_score}\n"
                           f"{game.winner}")

    @commands.command()
    async def hit(self,ctx):
        if f'{ctx.author.id}' in blackjack.gamelist:
            game = blackjack.gamelist[f'{ctx.author.id}']
            game.hit()
            await ctx.send(f"{game.dealer_hand},{game.player_hand}\n"
                           f"{game.dealer_score,game.player_score}\n"
                           f"{game.winner}")
    @commands.command()
    async def stay(self,ctx):
        if f'{ctx.author.id}' in blackjack.gamelist:
            game = blackjack.gamelist[f'{ctx.author.id}']
            game.stay()
            await ctx.send(f"{game.dealer_hand},{game.player_hand}\n"
                           f"{game.dealer_score,game.player_score}\n"
                           f"{game.winner}")rusrus
            game.end_game()
    @commands.command()
    async def check(self,ctx):
        await ctx.send(f"{len(blackjack.gamelist)}")



def setup(bot):
    bot.add_cog(games(bot))
