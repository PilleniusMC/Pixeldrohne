import discord
from discord.ext import commands
import asyncio
import youtube_dl
import random


class Voice:

    def __init__(self, bot):

        self.bot = bot
        self.channels = [
            "http://stream01.iloveradio.de/iloveradio1.mp3,I Love Radio,iloveradio",
            "http://br-br1-obb.cast.addradio.de/br/br1/obb/mp3/128/stream.mp3,Bayern 1,bayern1",
            "http://mp3channels.webradio.antenne.de:80/antenne,Antenne Bayern,antenne",
            "http://fhin.4broadcast.de/galaxyin.mp3,Radio Galaxy,radiogalaxy",
            "http://hr-youfm-live.cast.addradio.de/hr/youfm/live/mp3/128/stream.mp3,YOU FM,youfm",
            "http://mp3.planetradio.de/planetradio/hqlivestream.mp3,Planet Radio,planetradio",
            "http://mp3channels.webradio.antenne.de/rockantenne,ROCK ANTENNE,rockantenne",
            "http://mp3stream7.apasf.apa.at:8000,Ö3,oe3",
            "http://raj.krone.at:80/kronehit-ultra-hd.aac,Kronehit,krone",
            "http://radio.vgmradio.com:8040/stream,VGM Radio,vgm",
            "http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio1_mf_p,BBC Radio 1,bbc1",
            "http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio2_mf_p,BBC Radio 2,bbc2",
            "http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio3_mf_p,BBC Radio 3,bbc3",
            "http://us2.internet-radio.com:8281/live,Bollywood,bollywood",
            "http://64.71.79.181:8040/,Big B Korea,bigb-k",
            "http://64.71.79.181:8018/,Big B Japan,bigb-j",
            "http://ibizaglobalradio.streaming-pro.com:8024/,Ibiza Global Radio,ibiza"
        ]

        self.ytdl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': "mp3",
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }


        self.ffmpeg_opts = " -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"

        self.ytdl = youtube_dl.YoutubeDL(self.ytdl_opts)

        self.data = None
        self.title = None
        self.url = None

        self.states = {}
        self.queue = {}

    async def get_stream(self, song: str):

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(song, download=False))

        if song.lower().startswith("https://youtu"):

            return data
        else:

            return data['entries'][0]

    def radio(self, radio_channel):

        if radio_channel == "iloveradio":

            return "http://stream01.iloveradio.de/iloveradio1.mp3,I Love Radio"
        elif radio_channel == "bayern1":

            return "http://br-br1-obb.cast.addradio.de/br/br1/obb/mp3/128/stream.mp3,Bayern 1"
        elif radio_channel == "antenne":

            return "http://mp3channels.webradio.antenne.de:80/antenne,Antenne Bayern"
        elif radio_channel == "radiogalaxy":

            return "http://fhin.4broadcast.de/galaxyin.mp3,Radio Galaxy"
        elif radio_channel == "youfm":

            return "http://hr-youfm-live.cast.addradio.de/hr/youfm/live/mp3/128/stream.mp3,YOU FM"
        elif radio_channel == "planetradio":

            return "http://mp3.planetradio.de/planetradio/hqlivestream.mp3,Planet Radio"
        elif radio_channel == "rockantenne":

            return "http://mp3channels.webradio.antenne.de/rockantenne,ROCK ANTENNE"
        elif radio_channel == "oe3":

            return "http://mp3stream7.apasf.apa.at:8000,Ö3,oe3"
        elif radio_channel == "krone":

            return "http://raj.krone.at:80/kronehit-ultra-hd.aac,Kronehit"
        elif radio_channel == "vgm":

            return "http://radio.vgmradio.com:8040/stream,VGM Radio"
        elif radio_channel == "bbc1":

            return "http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio1_mf_p,BBC Radio 1"
        elif radio_channel == "bbc2":

            return "http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio2_mf_p,BBC Radio 2"
        elif radio_channel == "bbc3":

            return "http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio3_mf_p,BBC Radio 3"
        elif radio_channel == "bollywood":

            return "http://us2.internet-radio.com:8281/live,Bollywood"
        elif radio_channel == "ibiza":

            return "http://ibizaglobalradio.streaming-pro.com:8024/,Ibiza Global Radio"
        elif radio_channel == "bigb-k":

            return "http://64.71.79.181:8040/,Big B Korea"
        elif radio_channel == "bigb-j":

            return "http://64.71.79.181:8018/,Big B Japan"
        elif radio_channel == "random":

            return random.choice(self.channels)
        elif radio_channel == "list":

            return "EMBED"
        else:

            return "NOPE"

    @commands.command(no_pm=True)
    async def join(self, ctx):

        try:

            if ctx.guild.voice_client is not None:

                try:

                    voice = ctx.guild.voice_client
                    await voice.disconnect()
                except AttributeError:

                    await ctx.channel.send(embed=discord.Embed(color=discord.Color.red(), description="Error: Not connected to any voice channel"))
                except Exception as error:

                    await ctx.channel.send(embed=discord.Embed(color=discord.Color.red(), description=f"Error: `{error}`"))
            if ctx.message.guild.voice_client is None:

                try:

                    await ctx.author.voice.channel.connect()
                except AttributeError:

                    await ctx.channel.send(embed=discord.Embed(color=discord.Color.red(), description="Error: You aren't connected to any voice channel"))
                except Exception as error:

                    await ctx.channel.send(embed=discord.Embed(color=discord.Color.red(), description=f"Error: `{error}`"))
        except Exception as error:

            await ctx.channel.send(embed=discord.Embed(color=discord.Color.red(), description=f"Error: `{error}`"))

    @commands.command(no_pm=True)
    async def leave(self, ctx):

        try:

            voice = ctx.guild.voice_client
            await voice.disconnect()
        except AttributeError:

            await ctx.channel.send(embed=discord.Embed(color=discord.Color.red(), description="Error: Not connected to any voice channel"))
        except Exception as error:

            await ctx.channel.send(embed=discord.Embed(color=discord.Color.red(), description=f"Error: `{error}`"))

    @commands.command(no_pm=True)
    async def pause(self, ctx):

        try:

            self.states[str(ctx.guild.id)].pause()
        except Exception as error:

            await ctx.channel.send(f"Error: {error}")

    @commands.command(no_pm=True)
    async def resume(self, ctx):

        try:

            self.states[str(ctx.guild.id)].resume()
        except Exception as error:

            await ctx.channel.send(f"Error: {error}")

    @commands.command(no_pm=True)
    async def stop(self, ctx):

        try:

            self.states[str(ctx.guild.id)].stop()
        except Exception as error:

            await ctx.channel.send(f"Error: {error}")

    @commands.command(no_pm=True)
    async def volume(self, ctx, volume: str):

        try:

            volume = int(volume) if len(volume) > 0 else ctx.guild.voice_client.source.volume

            player_volume = volume / 100
        except:

            await ctx.channel.send("Please enter a valid ammount for the volume")
            return

        try:
            if player_volume <= 1.0:

                ctx.guild.voice_client.source.volume = player_volume
                await ctx.channel.send(f"Volume was set to {volume}%")
            elif player_volume > 1.0:

                await ctx.channel.send(f"Error: The volume you are trying to set is too high")
        except AttributeError:

            await ctx.channel.send("You aren't connected to any voice channel or the bot isn't playing at the moment")
        except Exception as error:

            await ctx.channel.send(f"Error: {error}")

    @commands.command(no_pm=True)
    async def mute(self, ctx):

        try:

            if 0.0 < ctx.guild.voice_client.source.volume <= 1.0:

                ctx.guild.voice_client.source.volume = 0.0
                await ctx.channel.send(f"The player was muted successfully")
            elif ctx.guild.voice_client.source.volume == 0.0:

                await ctx.channel.send("The player is already muted")
            else:

                await ctx.channel.send("An error occured")
        except AttributeError:

            await ctx.channel.send("You aren't connected to any voice channel or the bot isn't playing at the moment")
        except Exception as error:

            await ctx.channel.send(f"Error: {error}")

    @commands.command(name="radio", no_pm=True)
    async def play_radio(self, ctx, *, radio_channel: str):

        radio_url = self.radio(radio_channel=radio_channel)

        if radio_url == "NOPE":

            await ctx.channel.send(f"Sorry, this is an unknown channel. For a list of valid channels, please type `{self.bot.command_prefix}radio list`")
            return
        elif radio_url == "EMBED":
            embed = discord.Embed(
                title="Radiosender",
                description="Das hier ist die aktuelle Liste an Radiosendern, die der Bot abspielen kann.",
                color=0x22a64b
            )
            for i in self.channels:
                url, channel, argument = i.split(",")
                embed.add_field(name=argument, value=channel)
            await ctx.channel.send(embed=embed)
            return
        else:

            radio_url, channel = self.radio(radio_channel=radio_channel).split(",")

            if ctx.guild.voice_client is not None:

                try:

                    voice = ctx.guild.voice_client

                    self.states[str(ctx.guild.id)].stop()

                    player = discord.FFmpegPCMAudio(radio_url, before_options=self.ffmpeg_opts)
                    self.states[str(ctx.guild.id)] = voice

                    source = discord.PCMVolumeTransformer(player)
                    voice.play(source)

                    await ctx.channel.send(f"Now playing: {channel}")
                except Exception as error:

                    await ctx.channel.send(f"Error: {error}")

            elif ctx.guild.voice_client is None:

                try:

                    await ctx.invoke(self.join)

                    voice = ctx.guild.voice_client

                    player = discord.FFmpegPCMAudio(radio_url, before_options=self.ffmpeg_opts)
                    self.states[str(ctx.guild.id)] = voice

                    source = discord.PCMVolumeTransformer(player)
                    voice.play(source)

                    await ctx.channel.send(f"Now playing: {channel}")
                except Exception as error:

                    await ctx.channel.send(f"Error: {error}")

    @commands.command(name="play", no_pm=True)
    async def play_yt(self, ctx, *, song: str):

        if ctx.guild.voice_client is not None:

            try:

                voice = ctx.guild.voice_client

                self.data = await self.get_stream(song)

                data = self.data['formats'][0]
                yt_stream = data['url']

                self.states[str(ctx.guild.id)] = voice

                try:

                    if len(self.queue[str(ctx.guild.id)]) > 0:

                        pass
                    else:

                        self.queue[str(ctx.guild.id)] = []
                except KeyError:

                    self.queue[str(ctx.guild.id)] = []
                self.queue[str(ctx.guild.id)].append(yt_stream)
                await ctx.send("Song has been added to the queue")

                for stream in self.queue[str(ctx.guild.id)]:

                    while self.states[str(ctx.guild.id)].is_playing() or self.states[str(ctx.guild.id)].is_paused():
                        await asyncio.sleep(1)

                    if not self.states[str(ctx.guild.id)].is_playing() or self.states[str(ctx.guild.id)].is_paused():

                        player = discord.FFmpegPCMAudio(self.queue[str(ctx.guild.id)].pop(0),
                                                        before_options=self.ffmpeg_opts)
                        source = discord.PCMVolumeTransformer(player)
                        voice.play(source)

                        await ctx.send("Playback gestartet")
                    elif self.states[str(ctx.guild.id)].is_playing() or self.states[str(ctx.guild.id)].is_paused():

                        pass
            except Exception as error:

                await ctx.send(f"Error: {error}")
        elif ctx.guild.voice_client is None:

            try:

                await ctx.invoke(self.join)

                voice = ctx.guild.voice_client

                self.data = await self.get_stream(song)

                data = self.data['formats'][0]
                yt_stream = data['url']

                self.states[str(ctx.guild.id)] = voice

                player = discord.FFmpegPCMAudio(yt_stream, before_options=self.ffmpeg_opts)
                source = discord.PCMVolumeTransformer(player)
                voice.play(source)

                await ctx.send("Tick Tick")
            except Exception as error:

                await ctx.send(f"Error: {error}")
                
def setup(bot: commands.Bot):
    bot.add_cog(Voice(bot=bot))
                
