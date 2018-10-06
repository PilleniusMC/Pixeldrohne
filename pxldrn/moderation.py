import discord
from discord.ext import commands
from datetime import datetime


class Mods:
    def __init__(self, bot):
        self.bot = bot
        self.color = 0xf0aade

    @commands.command(name="kick", no_pm=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *arg):
        if arg == ():
            reason = "Der Nutzer wurde vom Server geworfen."
        else:
            reason = " ".join(arg)
        embed = discord.Embed(
            title="Kick",
            description=f"Der Nutzer {user.name} wurde mit dem Grund `{reason}` gekicked.",
            color=self.color
        )
        await discord.Guild.kick(ctx.guild, user=user, reason=reason)
        await ctx.channel.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Es schaut fast so aus als sei der Nutzer nicht mehr auf dem Server.')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Nutzer konnte nicht gekicked werden.')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry, du kannst diesen Befehl leider nicht nutzen.')

    @commands.command(name="ban", no_pm=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *arg):
        if arg == ():
            reason = "Der Nutzer wurde vom Server geworfen."
        else:
            reason = " ".join(arg)
        embed = discord.Embed(
            title="Ban",
            description=f"Der Nutzer {user.name} wurde mit dem Grund `{reason}` gebannt.",
            color=self.color
        )
        await discord.Guild.kick(ctx.guild, user=user, reason=reason)
        await ctx.channel.send(embed=embed)

    @ban.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Es schaut fast so aus als sei der Nutzer nicht mehr auf dem Server.')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Nutzer konnte nicht gebannt werden.')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry, du kannst diesen Befehl leider nicht nutzen.')

    @commands.command(name="purge", no_pm=True)
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(5, 10, commands.BucketType.default)
    async def purge(self, ctx, messages: int):
        if messages > 150:
            await ctx.send("So viele Nachrichten kann ich leider nicht löschen.")
        else:
            messages = messages + 1
            deleted = await ctx.channel.purge(limit=messages, bulk=True)
            await ctx.channel.send(f"Es wurden erfolgreich {len(deleted)-1} Nachrichten gelöscht.", delete_after=5)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry, du kannst diesen Befehl leider nicht nutzen.')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Bitte, gib eine Nachrichtenanzahl an.')
        if isinstance(error, commands.CommandOnCooldown):
            await  ctx.send("Bitte warte kurz bevor du diesen Befehl wieder nutzt.\nLeider unterliege ich Rate-Limits")


class Admin:
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x0d8dff
        self.prefix = bot.command_prefix

    @commands.group(name="startup", no_pm=True)
    # @commands.has_permissions(administrator=True)
    async def startup(self, ctx):
        if ctx.invoked_subcommand is None:
            async with ctx.typing():
                bot_mem = ctx.guild.get_member(self.bot.user.id)
                perms = bot_mem.guild_permissions
                stperm = discord.Embed(
                    title="Startup:",
                    timestamp=datetime.utcnow(),
                    description=f"Danke, dass du dich für den Bot {self.bot.user.name} entschieden hast.\nFolgend sind alle"
                                f" Rechte, die der Bot hat bzw. nicht hat, und welche Befehle dadurch genutzt werden können"
                                f" oder eben nicht genutzt werden können.\nWenn du den Bot auf einen Kanal begrenzt hast"
                                f" oder Befehle nur in dem Kanal genutzt werden sollen nutze "
                                f"bitte `{self.bot.command_prefix}startup channel`.",
                    color=self.color
                )
                stperm.set_author(name=bot_mem.name, icon_url=self.bot.user.avatar_url, url="https://pixeldrohne.mystic-alchemy.com")
                stperm.set_footer(text="Dieses Embed hat den Stand von")
                stperm.add_field(name="Die höchste Rolle des Bots:", value=bot_mem.top_role.name, inline=False)
                if perms.administrator:
                    stperm.add_field(name="Warnung: Bots sollten kein Administrator haben, da dies ein gewisses "
                                          "Sicherheitsrisiko birgt!", value="Bitte entferne Administrator vom Bot.",
                                     inline=False)
                    stperm.add_field(name="Kicken ✅", value=f"{self.prefix}kick <member>")
                    stperm.add_field(name="Bannen ✅", value=f"{self.prefix}ban <member>")
                else:
                    if perms.attach_files:
                        stperm.add_field(name="Dateien anhängen ✅", value=f"{self.prefix}gif <suche>\n{self.prefix}avatar [member]")
                    else:
                        stperm.add_field(name="Dateien anhängen ❌", value=f"{self.prefix}gif <suche>\n{self.prefix}avatar [member]")
                    if perms.manage_messages:
                        stperm.add_field(name="Nachrichten verwalten ✅", value=f"{self.prefix}purge\nVerschiedene Befehle")
                    else:
                        stperm.add_field(name="Nachrichten verwalten ❌", value=f"{self.prefix}purge")
                    if perms.manage_roles:
                        stperm.add_field(name="Rollen verwalten ✅", value=f"Platzhalter für einen\nMute Befehl")
                    else:
                        stperm.add_field(name="Rollen verwalten ❌", value=f"Platzhalter für einen\nMute Befehl")
                    if perms.kick_members:
                        stperm.add_field(name="Kicken ✅", value=f"{self.prefix}kick <member>")
                    else:
                        stperm.add_field(name="Kicken ❌", value=f"{self.prefix}kick <member>")
                    if perms.ban_members:
                        stperm.add_field(name="Bannen ✅", value=f"{self.prefix}ban <member>")
                    else:
                        stperm.add_field(name="Bannen ❌", value=f"{self.prefix}ban <member>")

                await ctx.send("Server Perms: " + str(perms.value), embed=stperm)
                return

    @startup.error
    async def startup_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Bitte einen Administrator diesen Befehl zu nutzen.")

    @startup.command(name="channel")
    async def startup_channel(self, ctx):
        bot_mem = ctx.guild.get_member(self.bot.user.id)
        perms = discord.abc.GuildChannel.permissions_for(ctx.channel, bot_mem)
        await ctx.send("Channel Perm: " + str(perms.value))

def setup(bot: commands.Bot):
        bot.add_cog(Mods(bot=bot))
