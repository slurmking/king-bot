#  Copyright (c)Slurmking 2020

import asyncio
import configparser
import re
import logging
import discord
import googleapiclient.discovery
import lavalink
import spotipy
from discord.ext import commands
from spotipy.oauth2 import SpotifyClientCredentials

from req import database

url_rx = re.compile(r'https?://(?:www\.)?.+')
config = configparser.ConfigParser()
config.read('setup/config.ini')
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config['api']['spotiftyid'],
                                                           client_secret=config['api']['spotifysecret']))
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=config['api']['youtubekey'])


async def findtracks(query, player, ctx):
    player = player
    ctx = ctx
    if not url_rx.match(query):
        query = f'ytsearch:{query}'
    results = await player.node.get_tracks(query)
    track = results['tracks'][0]
    track = lavalink.models.AudioTrack(track, ctx.author.id)
    return track
    # player.add(requester=ctx.author.id, track=track)


async def loadtracks(request, player, ctx, message):
    songs = []
    for index, item in enumerate(request):
        if len(player.queue) + (index + 1) > 99:
            break
        songs.append(asyncio.create_task(findtracks(item, player, ctx)))

    songbuffer = (await asyncio.gather(*songs))
    for song in songbuffer:
        player.add(requester=ctx.author.id, track=song)
    if len(songs) == 1:
        await message.edit(content=f'Added: {songbuffer[0].title}')
    else:
        await message.edit(content=f'{len(songs)} Songs Added')



async def youtube_search(query):
    response_list = []
    query = '+'.join(query)

    request = youtube.search().list(
        part="snippet",
        maxResults=25,
        q=f"{query}"
    )
    response = request.execute()
    for x in range(1,6):
        print(x)
        video_id = response['items'][x]['id']['videoId']
        title = response['items'][x]['snippet']['title']
        response_list.append({'title': title, 'url': f'https://www.youtube.com/watch?v={video_id}'})
    print(video_id)
    print(response['items'][0]['snippet']['title'])
    return response_list
# response_list.append({'title': title,'url': f'https://www.youtube.com/watch?v={id_youutube_search}'})


async def url_convert(arg):
    output = []
    url = str(' '.join(arg[:]))
    if url.startswith('https://open.spotify.com'):
        type_url_conver = (url.split('/')[3])
        id_url_convert = ((url.split('/')[4]).split('?')[0])
        if type_url_conver == 'track':
            return spotify_track(id_url_convert)
        elif type_url_conver == 'album':
            return spotify_album(id_url_convert)
        elif type_url_conver == 'playlist':
            return spotify_playlist(id_url_convert)
        else:
            pass
    elif url.startswith('https://www.youtube.com/'):
        output.append(f"{url}")
        return output
    else:
        output.append(f"{arg}")
        return output


def spotify_track(id_spotif_track):
    results = sp.track(id_spotif_track)
    output = [f"{results['name']} {results['artists'][0]['name']}"]
    return output


def spotify_playlist(id_spotify_playlist):
    results = sp.playlist(id_spotify_playlist)
    output = []
    for x in range(len(results['tracks']['items'])):
        track = results['tracks']['items'][x]['track']
        output.append(f"{track['name']} {track['artists'][0]['name']}")
    return output


def spotify_album(id_spotify_album):
    results = sp.album(id_spotify_album)
    output = []
    for x in range(len(results['tracks']['items'])):
        output.append(
            f"{results['tracks']['items'][x]['name']} {results['tracks']['items'][x]['artists'][0]['name']}")
    return output


# noinspection PyTypeChecker
class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info(f"\033[92m[COG]\033[0m{self.qualified_name}:loaded")
        if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(bot.user.id)
            for client in range(1, int(config['lavalink_clients']['count']) + 1):
                client = (config[f'lavalink{client}'])
                bot.lavalink.add_node(client['ip'], int(client['port']), client['pass'], client['region'],
                                      client['name'])  # Host, Port, Password, Region, Name
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

        lavalink.add_event_hook(self.track_hook)

    async def cog_before_invoke(self, ctx):
        role_check = database.cache_dj(ctx.guild.id)
        exceptions = ['q', 'dj']
        guild_check = ctx.guild is not None
        if not guild_check:
            return False
        if ctx.command.name in exceptions:
            return True
        elif role_check != 'None':
            dj_role = (ctx.guild.get_role(int(role_check)))
            if dj_role in ctx.author.roles:
                await self.ensure_voice(ctx)
                return True
            else:
                await ctx.send(f'You do not have [{dj_role.name}] role')
                return False
        else:
            await self.ensure_voice(ctx)
            return True

    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        # Create returns a player if one exists, otherwise creates.
        # This line is important because it ensures that a player always exists for a guild.

        # Most people might consider this a waste of resources for guilds that aren't playing, but this is
        # the easiest and simplest way of ensuring players are created.

        # These are commands that require the bot to join a voicechannel (i.e. initiating playback).
        # Commands such as volume/skip etc don't require the bot to be in a voicechannel so don't need listing here.
        should_connect = ctx.command.name in ('play',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            # Our cog_command_error handler catches this and sends it to the voicechannel.
            # Exceptions allow us to "short-circuit" command invocation via checks so the
            # execution state of the command goes no further.
            ctx.send('Join a voicechannel first.')
        if not player.is_connected:
            if not should_connect:
                await ctx.send('Not connected.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                ctx.send('I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                ctx.send('You need to be in my voicechannel.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            # When this track_hook receives a "QueueEndEvent" from lavalink.py
            # it indicates that there are no tracks left in the player's queue.
            # To save on resources, we can tell the bot to disconnect from the voicechannel.
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        """ Connects to the given voicechannel ID. A channel_id of `None` means disconnect. """
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id, self_deaf=True)
        # The above looks dirty, we could alternatively use `bot.shards[shard_id].ws` but that assumes
        # the bot instance is an AutoShardedBot.

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            # When this track_hook receives a "QueueEndEvent" from lavalink.py
            # it indicates that there are no tracks left in the player's queue.
            # To save on resources, we can tell the bot to disconnect from the voicechannel.
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    @commands.command(aliases=['p'], brief='plays song', help='Search for song via youtube/spotify url, or search term')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def play(self, ctx, *arg):
        await ctx.message.delete()
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if player.paused:
            await player.set_pause(False)
        else:
            message = await ctx.send('Loading songs')
            request = await url_convert(arg)
            try:
                await loadtracks(request, player, ctx, message)
            except IndexError:
                ctx.send('Couldn\'t Find song')
            await asyncio.sleep(1)
            self.play.reset_cooldown(ctx)
            if not player.is_playing:
                await player.play()

    @commands.command(help='Shows the currently playing song')
    async def np(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        now_playing = player.current
        if not now_playing:
            ctx.send('Nothing is currently playing')
        else:
            pass
        if not now_playing.stream:
            song_percent = (player.position / now_playing.duration)
            play_bar = []
            for _ in range(1, 11):
                # song percent less than 10
                if song_percent * 10 < 1 and _ < 2:
                    play_bar.append('🟢')
                # song percent more than range and song percent more than range *10
                elif _ <= song_percent * 10 < _ + 1:
                    play_bar.append('🟢')
                else:
                    play_bar.append('─')
            s = ''
            scrubber = (
                f"     {lavalink.format_time(player.position)} / "
                f"{lavalink.format_time(now_playing.duration)}\n[{s.join(play_bar)}]")
        else:
            scrubber = 'Streaming'
        embed = discord.Embed(colour=discord.Colour(
            0x246b76), url=now_playing.uri)
        embed.set_author(name=now_playing.title, url=now_playing.uri)
        embed.description = f"{scrubber}"
        # embed.set_footer(text=f"Added by: {self.bot.get_user(now_playing.requester).display_name}")
        print(self.bot.get_user(now_playing.requester))
        if now_playing.uri.startswith('https://www.youtube'):
            embed.set_thumbnail(url=f'https://img.youtube.com/vi/{now_playing.identifier}/mqdefault.jpg')
        await ctx.message.delete()
        await ctx.send(embed=embed, delete_after=60)

    @commands.command(help="Get song queue", aliases=['q'])
    async def queue(self, ctx):
        try:
            player = self.bot.lavalink.player_manager.get(ctx.guild.id)
            track_list = []
            for item in player.queue:
                if len(item.title) > 29:
                    track_list.append(f"{item.title[:30]}...")
                else:
                    track_list.append(item.title)
            now_playing = player.current
            length = len(track_list)
            max_page = (-(-length // 10))
            page_content = []
            shuffle_state = ""
            loop_state = ""
            if player.repeat:
                loop_state = " (Loop Enabled)"
            if player.shuffle:
                shuffle_state = " (Shuffle Enabled)"
            # check if queue has items
            for n in range(0, max_page):
                top = (10 * n) + 10
                if top > length:
                    top = length
                page_content.append(track_list[10 * n:top])
                for p in range(0, (len(page_content[n]))):
                    page_content[n][p] = f"{n * 10 + p + 1}: {page_content[n][p]}\n"
            cur_page = 1
            header = f'Now Playing :: {now_playing.title}{loop_state} [{lavalink.format_time(now_playing.duration)}]'
            message = await ctx.send(
                f"```asciidoc\n{header}\n== Page {cur_page}/{max_page}"
                f" ==\n{''.join(page_content[int(cur_page) - 1])}\n{length} :: songs total{shuffle_state}```")
            # getting the message object for editing and reacting
        except (UnboundLocalError, AttributeError):
            ctx.send('No songs queued')

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction_check, user_check):
            return user_check == ctx.author and str(reaction_check.emoji) in ["◀️", "▶️"]
            # This makes sure nobody except the command sender can interact with the "menu"

        await ctx.message.delete()
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "▶️" and cur_page != max_page:
                    cur_page += 1
                    await message.edit(
                        content=f"```asciidoc\n{header}\n"
                                f"== Page {cur_page}/{max_page}"
                                f" ==\n{''.join(page_content[int(cur_page) - 1])}\n{length}"
                                f" :: songs total{shuffle_state}```")
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(
                        content=f"```asciidoc\n{header}\n"
                                f"== Page {cur_page}/{max_page}"
                                f" ==\n{''.join(page_content[int(cur_page) - 1])}\n{length} "
                                f":: songs total{shuffle_state}```")
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                break
            # ending the loop if user doesn't react after x seconds

    @commands.command(help='Shuffles player')
    async def shuffle(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if player.shuffle:
            player.set_shuffle(False)
        else:
            player.set_shuffle(True)
            await ctx.send("Shuffle Enabled")

    @commands.command(help='Loops song')
    async def loop(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if player.repeat:
            player.set_repeat(False)
        else:
            player.set_repeat(True)
            await ctx.send("Loop Enabled")

    @commands.command(help='Stops Player')
    async def stop(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        ws = self.bot._connection._get_websocket(ctx.guild.id)
        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild.id, None)
        await player.stop()

    @commands.command(help='Pauses song')
    async def pause(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        await player.set_pause(True)

    @commands.command(help='Resumes paused song')
    async def resume(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        await player.set_pause(False)

    @commands.command(help="Skips song")
    async def skip(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        await player.skip()

    @commands.command(help="Jumps to song")
    async def jump(self, ctx, arg):
        arg = int(arg)
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        await player.play(track=player.queue[arg - 1])
        del player.queue[0:arg]

    @commands.command(help="Removes song")
    async def remove(self, ctx, arg):
        arg = int(arg)
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        await ctx.send(f"Removing: {player.queue[arg - 1].title}")
        del player.queue[arg - 1]

    @commands.command(help="Inserts song next in line")
    async def insert(self, ctx, *arg):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        url = str(' '.join(arg[:]))
        request = await url_convert(url)
        if player.paused:
            await player.set_pause(False)
        else:
            message = await ctx.send('Loading songs')
            try:
                track = await findtracks(request[0], player, ctx)
                player.add(ctx.author.id, track, 0)
                await message.edit(content=f'{track.title} Inserted')
            except IndexError:
                await message.edit(content=f'Couldn\'t Find song')
            await asyncio.sleep(1)
            if not player.is_playing:
                await player.play()


    @commands.command(help="Clears song queue")
    async def clear(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        del player.queue[:]

    @commands.command(hidden=True)
    async def search(self, ctx, *arg):
        await youtube_search(arg)
        async with ctx.typing():
            info = await youtube_search(arg)
            results = []
            urls = []
            for index, _ in enumerate(info):
                if index < 5:
                    results.append(f"{index + 1}: {_['title']}")
                    urls.append(f"{_['url']}")
                else:
                    pass
            newline = '\n'
        message = await ctx.send(f"```\nSearch Results\n==============\n{newline.join(results)}\n```")
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        for _ in reactions:
            await message.add_reaction(f"{_}")

        def check(reaction_check, user_check):
            return user_check == ctx.author and str(reaction_check.emoji) in reactions

        while True:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example
            for index, _ in enumerate(reactions):
                try:
                    if str(reaction.emoji) == f"{_}":
                        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
                        results = await player.node.get_tracks(urls[index])
                        track = results['tracks'][0]
                        track = lavalink.models.AudioTrack(track, ctx.author.id)
                        player.add(requester=ctx.author.id, track=track)
                        await ctx.send(f'Added: {track.title}')
                        if not player.is_playing:
                            await player.play()
                        await message.delete()
                except asyncio.TimeoutError:
                    await message.delete()
                    break
                except IndexError:
                    ctx.send('Invalid Song')
        pass

    @commands.command(hidden=True)
    @commands.check(commands.is_owner())
    async def playerinfo(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        await ctx.send(f"```\nGuild Id: {player.guild_id}\n"
                       f"Node: {player.node}\n"
                       f"Paused: {player.paused}\n"
                       f"Shuffle:{player.shuffle}\n"
                       f"Repeat:{player.repeat}\n"
                       f"Queue:{len(player.queue)}\n"
                       f"Playing:{player.is_playing}\n```")

    @commands.command(hidden=True)
    @commands.check(commands.is_owner())
    async def managerinfo(self, ctx):
        node_manager = self.bot.lavalink.node_manager.nodes
        for node in node_manager:
            print(node.stats.memory_allocated / 1048576)
            print(node.stats.memory_used / 1048576)

    @commands.command(hidden=True)
    @commands.check(commands.is_owner())
    async def dj(self, ctx, arg):
        if arg == 'clear':
            database.update_guild(ctx.guild.id, 'dj_role', None)
            await ctx.send('DJ role requirement removed')
        else:
            database.update_guild(ctx.guild.id, 'dj_role', ctx.message.raw_role_mentions[0])
            await ctx.send(f'DJ set to [@{ctx.message.role_mentions[0]}]')


def setup(bot):
    bot.add_cog(music(bot))
