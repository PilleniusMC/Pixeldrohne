import random
import discord
from discord.ext import commands


def to_lower(argument):
    return str(argument.lower())


class SchereSteinPapier:

    def __init__(self, bot):

        self.bot = bot
        self.norm = ["schere", "stein", "papier"]
        self.ext = ["schere", "stein", "papier", "spock", "echse"]
        self.win_dict = {"schere": {"sieg": "papier", "verloren": "stein"},
                         "stein": {"sieg": "schere", "verloren": "papier"},
                         "papier": {"sieg": "stein", "verloren": "schere"}}
        self.win_dict_ext = {"schere": {"sieg": ["papier", "echse"], "verloren": ["stein", "spock"]},
                             "stein": {"sieg": ["schere", "echse"], "verloren": ["papier", "spock"]},
                             "papier": {"sieg": ["stein", "spock"], "verloren": ["schere", "echse"]},
                             "echse": {"sieg": ["papier", "spock"], "verloren": ["stein", "echse"]},
                             "spock": {"sieg": ["schere", "stein"], "verloren": ["papier", "echse"]}}

    async def ssp_embeds(self, ctx, status="n", bot=None, spieler=None):
        if status == "u":
            embed = discord.Embed(
                title="Wir haben das gleiche gewählt",
                description="Eigentlich hasse ich es ja, dass es auf ein Unentschieden rausläuft.",
                color=0xecde13
            )
            await ctx.send(embed=embed)
        elif status == "s":
            embed = discord.Embed(
                title="Du hast gewonnen.",
                description="😭 Ich habe verloren. 😭 Och menno! 😭 Ich wollte doch gewinnen. 😭",
                color=0x00ff00
            )
            embed.add_field(name="Bot", value=bot.capitalize())
            embed.add_field(name="Spieler", value=spieler.capitalize())
            await ctx.send(embed=embed)
        elif status == "v":
            embed = discord.Embed(
                title="Du hast verloren.",
                description="😁 Hihi, ich habe gewonnen. Aber keine Sorge du kannst dann vielleicht nächstes mal auch gewinnen. 😇",
                color=0xff0000
            )
            embed.add_field(name="Bot", value=bot.capitalize())
            embed.add_field(name="Spieler", value=spieler.capitalize())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Huch, da ist was schiefgegangen.",
                description="Da ist wohl in meinem System was falsch gelaufen, na klasse."
            )

    @commands.group(name="ssp", case_insensitive=True)
    async def ssp(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Bitte nenne mir Schere Stein Papier oder -e um mit Echse und Spock zu spielen")

    @ssp.command(name="schere")
    async def schere(self, ctx):
        bot_choice = random.choice(self.norm)
        if bot_choice == "schere":
            await self.ssp_embeds(ctx, status="u", bot=bot_choice, spieler="schere")
        elif bot_choice in self.win_dict['schere']['sieg']:
            await self.ssp_embeds(ctx, status="s", bot=bot_choice, spieler="schere")
        elif bot_choice in self.win_dict['schere']['verloren']:
            await self.ssp_embeds(ctx, status="v", bot=bot_choice, spieler="schere")
        else:
            await self.ssp_embeds(ctx)

    @ssp.command(name="stein")
    async def stein(self, ctx):
        bot_choice = random.choice(self.norm)
        if bot_choice == "stein":
            await self.ssp_embeds(ctx, status="u", bot=bot_choice, spieler="stein")
        elif bot_choice in self.win_dict['stein']['sieg']:
            await self.ssp_embeds(ctx, status="s", bot=bot_choice, spieler="stein")
        elif bot_choice in self.win_dict['stein']['verloren']:
            await self.ssp_embeds(ctx, status="v", bot=bot_choice, spieler="stein")
        else:
            await self.ssp_embeds(ctx)

    @ssp.command(name="papier")
    async def papier(self, ctx):
        bot_choice = random.choice(self.norm)
        if bot_choice == "papier":
            await self.ssp_embeds(ctx, status="u", bot=bot_choice, spieler="papier")
        elif bot_choice in self.win_dict['papier']['sieg']:
            await self.ssp_embeds(ctx, status="s", bot=bot_choice, spieler="papier")
        elif bot_choice in self.win_dict['papier']['verloren']:
            await self.ssp_embeds(ctx, status="v", bot=bot_choice, spieler="papier")
        else:
            await self.ssp_embeds(ctx)

    @ssp.command(name="-e")
    async def extended(self, ctx, wahl: to_lower):
        if wahl not in self.ext:
            await ctx.send("Bitte wähle zwischen Schere, Stein, Papier, Echse oder Spock.")
        else:
            bot_choice = random.choice(self.ext)
            if bot_choice == wahl:
                await self.ssp_embeds(ctx, status="u", bot=bot_choice, spieler=wahl)
            elif bot_choice in self.win_dict_ext[wahl]['sieg']:
                await self.ssp_embeds(ctx, status="s", bot=bot_choice, spieler=wahl)
            elif bot_choice in self.win_dict_ext[wahl]['verloren']:
                await self.ssp_embeds(ctx, status="v", bot=bot_choice, spieler=wahl)
            else:
                await self.ssp_embeds(ctx)

    @extended.error
    async def extended_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Bitte wähle zwischen Schere, Stein, Papier, Echse oder Spock.")

def setup(bot: commands.Bot):
    bot.add_cog(SchereSteinPapier(bot=bot))
            
