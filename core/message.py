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

    @commands.command(aliases=["привет", "hi"])
    async def welcome(self, ctx: commands.Context) -> None:
        await ctx.reply(f"Привет {ctx.chatter}!")

    @commands.command(aliases=["рандом"])
    async def random(self, ctx: commands.Context) -> None:
        await ctx.reply(f"{ctx.chatter} {random.randint(0, 100)}!")

    @commands.command(aliases=["тг", "tg", "тгк"])
    async def telegram(self, ctx: commands.Context) -> None:
        await ctx.reply(f"{ctx.chatter} ТГК: https://t.me/pingvinius_228")