import discord
from discord.ext import commands
import random


class Help:
    def __init__(self, bot):
        self.bot = bot
        self.color_help = 0x0affe0
        self.color_about = 0xd86f33
        self.footer_choices = ["Liest überhaupt jemand das hier unten?",
                               f"Deine zufällige Zahl ist: nicht existent",
                               "Hier sind so viele lustige Fakten, was meinst du wie viele?",
                               "[         ]",
                               "Dieser Bot ist zu 100 % Fairtrade.",
                               "Wusstest du schon, dass Delfine sich im Spiegel erkennen?",
                               "Wusstest du schon, dass Katzen in jedem ihrer Ohren 32 Muskeln haben?",
                               "Wusstest du schon, dass Shrimps ein Herz im Kopf haben?",
                               "Wusstest du schon, dass Feuerzeuge vor dem Streichholz erfunden worden sind?",
                               "Wusstest du schon, dass alle Eisbären linkshänder sind?",
                               "Wusstest du schon, dass es mehr als 200 Chilli-Arten gibt?",
                               "Wusstest du schon, dass mehr Menschen in der Wüste ertrinken als verdursten?",
                               "Wusstest du schon, dass das Horn eines Nashorns eigentlich nur ein Haar ist?",
                               "Wusstest du schon, dass Elefanten nicht springen können?",
                               "Wusstest du schon, dass das Blut eines Kraken blau ist?",
                               "Wusstest du schon, dass in New York mehr Iren leben als in Dublin?",
                               "Wusstest du schon, dass Honig normalerweise nicht verderben kann?",
                               "Wusstest du schon, dass britische Abgeordnete nicht im Parlament sterben dürfen?"]

    @commands.command(name="help", aliases=["hilfe"])
    async def help_base(self, ctx, *arg):
        if arg == ():
            he = discord.Embed(
                title="Kurze Erklärung über die Hilfe",
                description=f"Die Hilfe ist in mehrere Abschnitte aufgeteilt. Diese Abschnitte werden mit dem Befehl "
                            f"`{self.bot.command_prefix}help <argument>` aufgerufen werden. So kann der Teil über die "
                            f"Befehle um Musik abzuspielen mit `{self.bot.command_prefix}help musik` aufgerufen werden.\n\n"
                            f"Bei einigen Befehlen muss noch ein Argument mitgegeben werden. Argumente, die mit <> markiert sind,"
                            f" müssen angegeben werden. Mit [] markierte Argumente sind optional. Mit {'{}'} markierte Argumente "
                            f"müssen bei bestimmten optionalen Argumenten genutzt werden.",
                color=self.color_help
            )
            he.set_thumbnail(url=self.bot.user.avatar_url)
            he.set_footer(icon_url=self.bot.user.avatar_url, text=random.choice(self.footer_choices))
            he.add_field(name="allgemein", value="Alle Befehle ohne\nspezielle Kategorie")
            he.add_field(name="musik", value="Die Musikbefehle")
            he.add_field(name="minigames", value="Die Minigames")
            await ctx.channel.send(embed=he)
        elif arg[0].lower() == 'allgemein':
            ae = discord.Embed(
                title="Die allgemeinen Befehle:",
                description="Alle Befehle, die keine wirklich spezielle Kategorie haben.",
                color=self.color_help
            )
            ae.set_footer(icon_url=self.bot.user.avatar_url, text=random.choice(self.footer_choices))
            ae.set_thumbnail(url=self.bot.user.avatar_url)
            ae.add_field(name=f"{self.bot.command_prefix}help", value="Diese Hilfe")
            ae.add_field(name=f"{self.bot.command_prefix}about", value="Erklärung des Bots")
            ae.add_field(name=f"{self.bot.command_prefix}invite", value="Die Links um den Bot einzuladen")
            ae.add_field(name=f"{self.bot.command_prefix}zahl <min> <may>", value="Zufällige Zahl, zwischen\neinem Min und Max")
            ae.add_field(name=f"{self.bot.command_prefix}avatar [nutzer]", value="Ruft einen Avatar ab.")
            ae.add_field(name=f"{self.bot.command_prefix}gif <suche>", value="Ruft ein GIF ab.")
            ae.add_field(name=f"{self.bot.command_prefix}zitat [modus] {'{zitat}'}",
                         value="Wenn kein Modus angegeben ist, dann wird ein zufälliges Zitat abgerufen.\nDie Modi können write oder hidden sein.\n"
                               "Wenn der Modus write genutzt wird muss noch ein Zitat angegeben werden, dass der Liste hinzugefügt werden soll.")
            ae.add_field(name=f"{self.bot.command_prefix}uptime", value="Zeigt an wie lange\nder Bot schon\nonline ist.")
            await ctx.channel.send(embed=ae)
        elif arg[0].lower() == 'musik':
            me = discord.Embed(
                title="Die Musikbefehle:",
                description=f"Um diese Befehle auszuführen sollte man am besten schon in einem Sprachkanal sein.",
                color=self.color_help
            )
            me.set_thumbnail(url=self.bot.user.avatar_url)
            me.set_footer(icon_url=self.bot.user.avatar_url, text=random.choice(self.footer_choices))
            me.add_field(name=f"{self.bot.command_prefix}join", value="Bot in den Kanal holen.")
            me.add_field(name=f"{self.bot.command_prefix}leave", value="Um den Bot aus einem Sprachkanal\nrauszuwerfen.")
            me.add_field(name=f"{self.bot.command_prefix}pause", value="Die Wiedergabe pausieren.")
            me.add_field(name=f"{self.bot.command_prefix}resume", value="Die Widergabe fortsetzen.")
            me.add_field(name=f"{self.bot.command_prefix}stop", value="Die Wiedergabe stoppen.")
            me.add_field(name=f"{self.bot.command_prefix}volume", value="Die Wiedergabelautstärke ändern.")
            me.add_field(name=f"{self.bot.command_prefix}mute", value="Den Bot stummschalten.")
            me.add_field(name=f"{self.bot.command_prefix}radio <radio>",
                         value=f"Einen Radiosender abspielen.\n`{self.bot.command_prefix}radio list` ruft eine Senderliste ab.")
            me.add_field(name=f"{self.bot.command_prefix}play <yt-link/suche>",
                         value="Spielt YouTube Videos ab. Um den Befehl zu nutzen einfach nen Link oder eine Suche vorgeben.")
            await ctx.channel.send(embed=me)
        elif arg[0].lower() == 'minigames':
            me = discord.Embed(
                title="Die Minigames des Bots",
                description="Alle Minigames, die von Nutzern verwendet werden können",
                color=self.color_help
            )
            me.set_thumbnail(url=self.bot.user.avatar_url)
            me.set_footer(icon_url=self.bot.user.avatar_url, text=random.choice(self.footer_choices))
            me.add_field(name=f"{self.bot.command_prefix}ssp <wahl[-e]> {'{extended}'}",
                         value="Normales Schere Stein Papier und Extended mit Echse und Spock. Wenn -e genutzt wird, muss auch extended gesetzt sein.")
            await ctx.send(embed=me)
        else:
            pass

    @commands.command(name="about")
    async def about_panel(self, ctx):
        about_embed = discord.Embed(
            title="Über die Pixeldrohne",
            description="An der Pixeldrohne wir schon seit Oktober 2017 gearbeitet. Ursprünglich war der Bot als "
                        "universeller Bot für den Streamer Pixelwerfer gedacht hat sich dann aber hat sich dann "
                        "zu etwas einiges größerem entwickelt. Jetzt ist die Pixeldrohne schon eigentlich viel zu"
                        "groß, dass ich diese alleine aufrecht erhalten kann.",
            color=self.color_about
        )
        about_embed.set_author(name="Pixeldrohne", url="https://twitch.tv/pixeldrohne", icon_url=self.bot.user.avatar_url)
        about_embed.set_footer(text=random.choice(self.footer_choices), icon_url=self.bot.user.avatar_url)
        about_embed.set_thumbnail(url=self.bot.user.avatar_url)
        about_embed.add_field(name="Autor:", value="PilleniusMC")
        about_embed.add_field(name="Programmiersprache:", value="Python")
        about_embed.add_field(name="GitHub:", value="https://github.com/Mystic-Alchemy/Pixeldrohne")
        await ctx.channel.send(embed=about_embed)

    @commands.command(name="github")
    async def github_panel(self, ctx):
        github_embed = discord.Embed(
            title="GitHub:",
            description="https://github.com/Mystic-Alchemy/Pixeldrohne",
            color=self.color_about
        )
        await ctx.channel.send(embed=github_embed)

    @commands.command(name="invite")
    async def invite_panel(self, ctx):
        embed = discord.Embed(
            title="Bot auf deinen Server einladen|Invite the bot to your server",
            description="Einfach einem der folgenden Links folgen um den Bot auf deinen Server zu holen.\n\nJust follow "
                        "one of the following links to get the bot on your server.",
            color=self.color_about
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(icon_url=self.bot.user.avatar_url, text=random.choice(self.footer_choices))
        embed.add_field(name="Deutsch", value="https://pixeldrohne.mystic-alchemy.com/de-invite")
        embed.add_field(name="English/International", value="https://pixeldrohne.mystic-alchemy.com/en-invite\n"
                                                            "Warning: this bot isn't yet online.")
        await ctx.channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Help(bot=bot))
        
