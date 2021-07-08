#  Copyright (c)Slurmking 2020

import datetime
import math
from copy import deepcopy
from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks
import database


class Tools(commands.Cog):
    voiceCheckList = {}

    def __init__(self, bot):
        self.bot = bot
        self.sleep_check.start()
        print(f"\033[92m[COG]\033[0m{self.qualified_name}:loaded")

    async def cog_check(self, ctx):
        if ctx.channel.type == discord.ChannelType.private:
            return False
        else:
            return True

    @tasks.loop(seconds=1.0)
    async def sleep_check(self):
        search_list = database.sleep_timer_get()
        if len(search_list) > 0:
            for user in search_list:
                guild = self.bot.get_guild(int(user[2]))
                member = guild.get_member(int(user[0]))
                channel = guild.get_channel(int(user[1]))
                try:
                    for channel_member in channel.members:
                        if channel_member.id == member.id:
                            await member.edit(voice_channel=None)
                    database.sleep_timer_del(member.id)
                    print(f'Kicking {member} in {guild} from {channel}')
                except IndexError:
                    pass

    @commands.command(help="Set a sleep timer for VC via format !sleep 00:00", brief="Create VC sleep timer")
    async def sleep(self, ctx, time_sleep):
        time_sleep = (time_sleep.split(":", ))
        hours = int(time_sleep[0]) * 60
        minutes = hours + int(time_sleep[1])
        print(minutes)
        # Max time 12 hours
        if not minutes > 300:
            database.sleep_timer_set(ctx.author.id, ctx.author.voice.channel.id, int(minutes), ctx.guild.id)
            await ctx.send(f"{ctx.author.mention} I will disconnect you in **{time_sleep[0]}"
                           f"** hours and **{time_sleep[1]}** minutes")
        else:
            await ctx.send(f"Time must be less than 5 hours")

    @commands.command(help="Get server latency")
    async def ping(self, ctx):
        await ctx.reply(f"Server Latency: {(round(self.bot.latency * 1000, 3))} ms")

    @commands.command(help="Steal discord emote")
    async def steal(self, ctx):
        emoji = (ctx.message.content.split('<'))
        anim_flag = emoji[1][0]
        emoji_id = emoji[1].split(':')[2][0:-1]
        if anim_flag == 'a':
            await ctx.send(f"https://cdn.discordapp.com/emojis/{emoji_id}.gif?v=1")
        else:
            await ctx.send(f"https://cdn.discordapp.com/emojis/{emoji_id}.png?v=1")

    @commands.command(help="Gets user info")
    async def userinfo(self, ctx, user="1"):
        if user == "1":
            userid = ctx.author.id
            print(userid)
            user = await self.bot.fetch_user(userid)
            print(user)
        else:
            try:
                userid = int(ctx.message.mentions[0].id)
                user = await self.bot.fetch_user(userid)
            except:
                user = await self.bot.fetch_user(int(user))
        embed = discord.Embed(title=user.name,
                              description=f"{user.name}#{user.discriminator}")
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='User Creation Date', value=user.created_at)
        await ctx.send(embed=embed)
        print(f"{userid} {user}")

    @commands.command(help="Create a Poll")
    async def poll(self, ctx, *args):
        values = (ctx.message.content[5:].split('|'))
        if not len(values) > 6:

            letters = ['🇦', '🇧', '🇨', '🇩', '🇪']
            embed = discord.Embed(title=f"{values[0]}", colour=discord.Colour(0x45d78c),
                                  timestamp=datetime.utcnow())
            del values[0]

            for index, value in enumerate(values):
                embed.add_field(name=f"{letters[index]} {value}", value="_ _", inline=False)
            embed.set_footer(text=f"Created By {ctx.message.author.display_name}")
            message = await ctx.send(embed=embed)
            for index, value in enumerate(values):
                await message.add_reaction(f"{letters[index]}")
        else:
            await ctx.send("You can only make a poll with 5 options or less")


def setup(bot):
    bot.add_cog(Tools(bot))
