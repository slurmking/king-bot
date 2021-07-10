#  Copyright (c)Slurmking 2020

import datetime
from datetime import datetime
import logging
import discord
from discord.ext import commands, tasks
from bot.req import database


class COG(commands.Cog):
    voiceCheckList = {}

    def __init__(self, bot):
        self.bot = bot
        logging.info(f"\033[92m[COG]\033[0m{self.qualified_name}:loaded")

    async def cog_check(self, ctx):
        if ctx.channel.type == discord.ChannelType.private:
            return False
        else:
            return True

def setup(bot):
    bot.add_cog(Tools(bot))
