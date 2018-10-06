import discord
from discord.ext import commands

"""
Diese Datei ist dazu da, dass ihr schnell benutzerdefinierte Befehle dem Bot hinzuzufügen.


Alle Befehle müssen wie folgend aufbebaut werden:

@commands.command(name='<Mit was der Befehl ausgeführt wird>')
async def name(self, ctx):
    Der Inhalt des Befehls
    
Um Fehler Handling zu nutzen muss ein weiterer Teil hinzugefügt werden:

@name.error
async def name_error(self, ctx, error):
    if isinstance(error, <Fehler aus discord.errors oder commands.errors>:
        Was bei diesem Fehler passieren soll.
        
Weitere Informationen sind der discord.py Rewrite Dokumentation zu entnehmen.
https://discordpy.readthedocs.io/en/rewrite/
"""


class CustomCommands:
    def __init__(self, bot):
        self.bot = bot
        # Klassenweite Variablen bitte hier definieren als self.var = var

    # Alle Befehle hiernach hinzufügen


def setup(bot: commands.Bot):
    bot.add_cog(CustomCommands(bot=bot))
    
