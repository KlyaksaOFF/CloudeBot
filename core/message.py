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
        await ctx.reply("https://donatex.gg/donate/pingvinius")

    @commands.group(name="socials", invoke_fallback=True)
    async def socials_group(self, ctx: commands.Context) -> None:
        await ctx.reply(f"{ctx.chatter} Все соцсети: https://t.me/pingvinius_228")

    @socials_group.command(name="telegram", aliases=[
        "tg", "тг", "телеграм", "telega", "телега"
    ])
    async def social_telegram(self, ctx: commands.Context) -> None:
        await ctx.reply(f"{ctx.chatter} ТГК: https://t.me/pingvinius_228")

    @socials_group.command(name="discord", aliases=["discord", "дискорд", "дс"])
    async def social_discord(self, ctx: commands.Context) -> None:
        await ctx.reply(f"{ctx.chatter} Discord: https://discord.gg/WxSbxHXVsB")
