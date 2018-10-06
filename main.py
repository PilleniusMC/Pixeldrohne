# Um den gesamten Bot auszuführen muss nur noch die Datei genutzt werden

import asyncio
import aiohttp
import safygiphy
from datetime import datetime, time
import discord
import io
import matplotlib.pyplot as plt
import matplotlib
from discord.ext import commands
from custom_commands import CustomCommands
from database_test import MainCommands
import pxldrn
import functools
import keys
import random
import asyncpg

giphy = safygiphy.Giphy()
bot = commands.Bot(command_prefix=keys.prefix, case_insensitive=True)
bot.remove_command("help")
plt.rcParams.update({'figure.autolayout': True})
matplotlib.rc('xtick', labelsize=10)

@bot.event
async def on_ready():
    print("Bot-Info:\nName: " + bot.user.name + "\nId: " + str(bot.user.id))
    await bot.change_presence(activity=discord.Game(f"mit {bot.command_prefix}help"))
    global st_datetime
    st_datetime = datetime.now()


@bot.command(no_pm=True)
async def say(ctx, *, arg):
    await ctx.message.delete()
    time = 0.2 * len(arg.split(' '))
    async with ctx.channel.typing():
        await asyncio.sleep(time)
        await ctx.channel.send(arg)

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        await ctx.channel.send("Du musst mir schon etwas geben, dass ich sagen kann.", delete_after=3)


@bot.command()
async def würfel(ctx, augen: int, anzahl: int):
    if augen <= 100:
        if anzahl <= 1000000:
            async with ctx.channel.typing():
                def blocking():
                    liste = []
                    for i in range(anzahl):
                        rando = random.randint(1, augen)
                        liste.append(rando)
                    return liste

                partial = functools.partial(blocking)
                liste = await bot.loop.run_in_executor(None, partial)
                simple = []
                eyes = []
                for i in range(augen):
                    count = liste.count(i + 1)
                    eyes.append(i + 1)
                    simple.append(count)

                plt.bar(eyes, simple, tick_label=eyes)
                plt.xlabel('Augen')
                plt.ylabel('Anzahl')
                plt.title('zufällige Würfel')
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                await ctx.send(file=discord.File(buf, "plot.png"))
                plt.clf()
        else:
            await ctx.send("Why?")
    else:
        await ctx.send("Why?")

@würfel.error
async def würfel_error(ctx, error):
    if isinstance(error, ValueError):
        await ctx.send("Mit den Werten kann ich leider nicht arbeiten.")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Äh, ich brauche schon Zahlen.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Es tut mir leid, aber um zu funktionieren brauche ich die Anzahl an Augen **und** die Anzahl"
                       "der Würfe")


@bot.command(no_pm=True)
async def avatar(ctx, user: discord.Member):
    async with aiohttp.ClientSession() as session:
        async with session.get(user.avatar_url) as resp:
            img = await resp.read()
            await ctx.send(file=discord.File(img, 'avatar.gif'))


@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Sorry, den Avatar dieses Nutzers kann ich nicht abrufen")
    if isinstance(error, commands.MissingRequiredArgument):
        async with aiohttp.ClientSession() as session:
            async with session.get(ctx.message.author.avatar_url) as resp:
                img = await resp.read()
                await ctx.send(file=discord.File(img, 'avatar.gif'))


@bot.command(no_pm=True)
async def gif(ctx, *, arg):
    async with ctx.channel.typing():
        rgif = giphy.random(tag=arg)
        async with aiohttp.ClientSession() as session:
            async with session.get(str(rgif.get("data", {}).get('image_original_url'))) as resp:
                rgif = await resp.read()
                await ctx.send(file=discord.File(rgif, 'gif.gif'))


@gif.error
async def gif_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Irgendetwas ist schiefgegangen. Bitte versuche es nochmal")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Bitte gib einen Suchbegriff ein.")
    else:
        await ctx.send(str(error))


@bot.command(no_pm=True)
async def zahl(ctx, z_min: int, z_max: int):
    await ctx.send(f"Deine Zahl ist: {random.randint(z_min, z_max)}")


@zahl.error
async def zahl_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Du musst mir zwei Zahlen geben, die erste das Minimum, die zweite das Maximum.")


@bot.group()
async def zitat(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.channel.typing():
            with open('zitate.txt', 'a', encoding='utf-8') as file:
                auswahl = file.readlines()
                zitat = random.choice(auswahl)
                await ctx.send(zitat)


@zitat.command(name="hidden")
async def hidden(ctx):
    async with ctx.channel.typing():
        with open('zitate.txt', 'r', encoding='utf-8') as file:
            auswahl = file.readlines()
            file.close()
            zitat = random.choice(auswahl)
            await ctx.send(zitat, delete_after=10)


@zitat.command(name="write")
async def write(ctx, *, arg):
    if not arg is None:
        async with ctx.channel.typing():
            with open('zitate.txt', 'a', encoding='utf-8') as file:
                file.write("\n" + arg)
                file.close()
                await ctx.send(f"Dein Zitat `{arg}` wurde der Liste hinzugefügt")
    else:
        pass


@write.error
async def write_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Sorry, wenn du kein Zitat angibst, kann ich es auch nicht hinzufügen.")


@bot.command(no_pm=True)
async def uptime(ctx):
    result = datetime.now() - st_datetime
    resultd = datetime.utcfromtimestamp(result.total_seconds()).time()
    tstring = None
    if resultd.second == 1:
        tstring = f"{resultd.second} Sekunde"
    else:
        tstring = f"{resultd.second} Sekunden."
    if resultd.minute > 0:
        if resultd.minute == 1:
            tstring = f"{resultd.minute} Minute und " + tstring
        else:
            tstring = f"{resultd.minute} Minuten und " + tstring
    if resultd.hour > 0:
        if resultd.hour == 1:
            tstring = f"{resultd.hour} Stunde, " + tstring
        else:
            tstring = f"{resultd.hour} Stunden, " + tstring
    if result.days > 0:
        if result.days == 1:
            tstring = f"{result.days} Tag, " + tstring
        else:
            tstring = f"{result.days} Tagen " + tstring
    await ctx.send(f"Der Bot läuft schon seit {tstring}")

cogs = [
    'pxldrn.helps',
    'pxldrn.music',
    'pxldrn.moderation',
    'pxldrn.minigames',
    'custom_commands',
    'databas_test'
]
    
for cog in cogs:
    bot.load_extension(cog)
bot.run(keys.token)
