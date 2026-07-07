from typing import TYPE_CHECKING

import twitchio
from twitchio.ext import commands
import random

if TYPE_CHECKING:
    from .bot import Bot


class MyCommands(commands.Component):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage) -> None:
        print(f"[{payload.broadcaster.name}] - {payload.chatter.name}: {payload.text}")

    @commands.command()
    async def hi(self, ctx: commands.Context) -> None:
        await ctx.reply(f"Hi {ctx.chatter}!")

    @commands.command()
    async def random(self, ctx: commands.Context) -> None:
        await ctx.reply(f"{ctx.chatter} {random.randint(0, 100)}!")
