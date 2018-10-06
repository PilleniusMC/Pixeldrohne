import discord
from discord.ext import commands

import random
import asyncio
import asyncpg
import keys

class MainCommands:
    def __init__(self, bot):
        self.bot = bot

    async def database(self):
        login_data = {"user": "postgres", "password": "mottek", "database": "test", "host": "127.0.0.1", "port": "5433"}
        db = await asyncpg.create_pool(**login_data)
        return db

    @commands.command(name="test")
    async def test(self, ctx, *, arg):
        await ctx.send(arg)

    @commands.command(name="select")
    async def selectdb(self, ctx, *, id: int):
        query = 'SELECT * FROM test_table WHERE id = $1;'
        db = await self.database()
        row = await db.fetchrow(query, id)

        await ctx.send(f"Name: {row['name']}, ID: {row['id']}")

    @commands.command(name="update")
    async def updatedb(self, ctx, *, new_name: str):
        db = await self.database()
        con = await db.acquire()
        async with con.transaction():
            query = 'UPDATE test_table SET "name" = $1 WHERE id = 1234;'

            await db.execute(query, new_name)
        await db.release(con)

        await ctx.send(f"Name in der Datenbank wurde erfolgreich zu {new_name} geupdated!")

    @commands.command(name="insert")
    async def insertdb(self, ctx, *, name: str):
        db = await self.database()
        user_id = random.randint(1000, 9999)

        con = await db.acquire()
        async with con.transaction():
            query = 'INSERT INTO test_table (id, name) VALUES ($1, $2);'

            await db.execute(query, user_id, name)
        await db.release(con)

        await ctx.send(f"Neuer Eintrag in der Datenbank hinzugefügt:\nName: {name}, ID: {user_id}")
                       
def setup(bot: commands.Bot):
    bot.add_cog(MainCommands(bot=bot))
