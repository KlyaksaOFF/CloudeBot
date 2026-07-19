import random
from typing import TYPE_CHECKING

import twitchio
from twitchio.ext import commands

from .data import DISCORD, DONATE, NICKNAME, OWNER_ID, STOLB, SURVIVAL, TELEGRAM

if TYPE_CHECKING:
    from .bot import Bot


class MyCommands(commands.Component):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage) -> None:
        print(f"[{payload.broadcaster.name}] - {payload.chatter.name}: "
              f"{payload.text}")

    @commands.cooldown(rate=1, per=60, key=commands.BucketType.chatter)
    @commands.command(aliases=["привет", "hi", "hello"])
    async def welcome(self, ctx: commands.Context) -> None:
        await ctx.reply(f"Привет {ctx.chatter}!")

    @commands.cooldown(rate=3, per=60, key=commands.BucketType.chatter)
    @commands.command(aliases=["рандом", "случайно"])
    async def random(self, ctx: commands.Context) -> None:
        await ctx.reply(f"{ctx.chatter} {random.randint(0, 100)}!")

    @commands.cooldown(rate=3, per=60, key=commands.BucketType.chatter)
    @commands.command(aliases=["донат", "donats", "донаты", "donat"])
    async def donate(self, ctx: commands.Context) -> None:
        await ctx.reply(f"{ctx.chatter}, {DONATE}")

    @commands.cooldown(rate=3, per=60, key=commands.BucketType.chatter)
    @commands.command(aliases=["server", "сервер", "айпи"])
    async def ip(self, ctx: commands.Context) -> None:
        await ctx.reply(
            f"{ctx.chatter}, наши сервера:\n"
            f"Выживание - ({SURVIVAL})\n"
            f"Столбы - ({STOLB})")

    @commands.cooldown(rate=2, per=30, key=commands.BucketType.chatter)
    @commands.command(aliases=["tg", "тг", "тгк", "телеграм"])
    async def telegram(self, ctx: commands.Context) -> None:
        await ctx.reply(f"{ctx.chatter}, {TELEGRAM}")

    @commands.cooldown(rate=1, per=60, key=commands.BucketType.chatter)
    @commands.command(aliases=["дс", "disco", "дискорд"])
    async def discord(self, ctx: commands.Context) -> None:
        await ctx.reply(f"{ctx.chatter}, {DISCORD}")

    @commands.command(aliases=["закреп"])
    @commands.cooldown(rate=1, per=60, key=commands.BucketType.chatter)
    async def pin(self, ctx: commands.Context) -> None:
        await ctx.reply(f"Наш тгк: {TELEGRAM} - Конкурс/Оповещения о стримах!")

    @commands.cooldown(rate=2, per=30, key=commands.BucketType.chatter)
    @commands.command(aliases=["рб", "rb", "рбник", "друзьярб"])
    async def roblox_friend(self, ctx: commands.Context) -> None:
        await ctx.reply(f"{ctx.chatter}, {NICKNAME} - ник в роблоксе.")

    @commands.cooldown(rate=1, per=20, key=commands.BucketType.chatter)
    @commands.command(aliases=["tgsend"])
    async def tg_send(self, ctx: commands.Context, count: int) -> None:
        if ctx.author.id == str(OWNER_ID):
            for i in range(count):
                await ctx.send(f"Тгк: {TELEGRAM}")
            return
        else:
            return await ctx.reply("У вас нет доступа к данной команде.")
