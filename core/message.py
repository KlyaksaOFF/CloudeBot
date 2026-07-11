import random
from typing import TYPE_CHECKING

import twitchio
from twitchio.ext import commands

if TYPE_CHECKING:
    from .bot import Bot, OWNER_ID

OWNER_ID = 1393289917

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
        await ctx.reply(f"{ctx.chatter}, donatex.gg/donate/pingvinius")

    @commands.cooldown(rate=3, per=60, key=commands.BucketType.chatter)
    @commands.command(aliases=["server", "сервер", "айпи"])
    async def ip(self, ctx: commands.Context) -> None:
        await ctx.reply(
            f"{ctx.chatter}, наши сервера:\n"
            f"Выживание - (94.29.33.162:25566)\n"
            f"Столбы - (94.29.33.162:25567)")

    @commands.cooldown(rate=2, per=30, key=commands.BucketType.chatter)
    @commands.command(aliases=["tg", "тг", "тгк", "телеграм"])
    async def telegram(self, ctx: commands.Context) -> None:
        await ctx.reply(f"{ctx.chatter}, t.me/pingvinius_228")

    @commands.cooldown(rate=1, per=60, key=commands.BucketType.chatter)
    @commands.command(aliases=["дс", "disco", "дискорд"])
    async def discord(self, ctx: commands.Context) -> None:
        await ctx.reply(f"{ctx.chatter}, discord.gg/pqZ7BSEhJj")

    @commands.command(aliases=["закреп"])
    @commands.cooldown(rate=1, per=60, key=commands.BucketType.chatter)
    async def pin(self, ctx: commands.Context) -> None:
        await ctx.reply("Наш тгк: t.me/pingvinius228 - Конкурс/Оповещения о стримах!")

    @commands.cooldown(rate=2, per=30, key=commands.BucketType.chatter)
    @commands.command(aliases=["рб", "rb", "рбник", "друзьярб"])
    async def roblox_friend(self, ctx: commands.Context) -> None:
        await ctx.reply(f"{ctx.chatter}, KlyaksaOFF - ник в роблоксе.")

    @commands.cooldown(rate=1, per=20, key=commands.BucketType.chatter)
    @commands.command(aliases=["tgsend"])
    async def tg_send(self, ctx: commands.Context, count: int) -> None:
        if ctx.author.id == str(OWNER_ID):
            for i in range(count):
                await ctx.send("Тгк: t.me/pingvinius_228")
            return
        else:
            return await ctx.reply("У вас нет доступа к данной команде.")
