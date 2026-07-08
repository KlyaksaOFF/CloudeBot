import random
from typing import TYPE_CHECKING

import twitchio
from twitchio.ext import commands

if TYPE_CHECKING:
    from .bot import Bot


class MyCommands(commands.Component):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage) -> None:
        print(f"[{payload.broadcaster.name}] - {payload.chatter.name}: "
              f"{payload.text}")

    @commands.command(aliases=["привет", "hi", "hello"])
    async def welcome(self, ctx: commands.Context) -> None:
        await ctx.reply(f"Привет {ctx.chatter}!")

    @commands.command(aliases=["рандом"])
    async def random(self, ctx: commands.Context) -> None:
        await ctx.reply(f"{ctx.chatter} {random.randint(0, 100)}!")

    @commands.command(aliases=["донат", "donats", "донаты", "donat"])
    async def donate(self, ctx: commands.Context) -> None:
        await ctx.reply("donatex.gg/donate/pingvinius")

    @commands.command(aliases=["server", "сервер", "айпи"])
    async def ip(self, ctx: commands.Context) -> None:
        await ctx.reply(
            f"{ctx.chatter}, наши сервера:\n"
            f"Выживание - (94.29.33.162:25566)\n"
            f"Столбы - (94.29.33.162:25567)")

    @commands.command(aliases=["tg", "тг", "тгк", "телеграм"])
    async def telegram(self, ctx: commands.Context) -> None:
        await ctx.reply(f"{ctx.chatter}, t.me/cloudertw")

    @commands.command(aliases=["дс", "disco", "дискорд"])
    async def discord(self, ctx: commands.Context) -> None:
        await ctx.reply(f"{ctx.chatter}, discord.gg/pqZ7BSEhJj")


