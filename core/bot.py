import logging
import os

import asqlite
import twitchio
from aiohttp import payload
from dotenv import load_dotenv
from twitchio import eventsub
from twitchio.ext import commands, routines
from datetime import datetime, timedelta
from .message import MyCommands

load_dotenv()

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
BOT_ID = os.environ.get('BOT_ID')
OWNER_ID = os.environ.get('OWNER_ID')

LOGGER: logging.Logger = logging.getLogger("Bot")


class Bot(commands.AutoBot):
    def __init__(
    self, *, token_database: asqlite.Pool,
    subs: list[eventsub.SubscriptionPayload]
    ) -> None:

        self.token_database = token_database

        super().__init__(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            bot_id=BOT_ID,
            owner_id=OWNER_ID,
            prefix="!",
            subscriptions=subs,
            force_subscribe=True,
            case_insensitive=True,
        )

    async def setup_hook(self) -> None:
        await self.add_component(MyCommands(self))

    async def event_oauth_authorized(
    self,
    payload: twitchio.authentication.UserTokenPayload
    ) -> None:

        await self.add_token(payload.access_token, payload.refresh_token)

        if not payload.user_id:
            return

        # Список подписок, которые мы хотели бы оформить
        # на недавно авторизованный канал
        subs: list[eventsub.SubscriptionPayload] = [
            eventsub.ChatMessageSubscription(
                broadcaster_user_id=payload.user_id,
                user_id=self.bot_id),
            eventsub.ChannelFollowSubscription(
                broadcaster_user_id=payload.user_id,
                moderator_user_id=self.bot_id,
            ),
            eventsub.StreamOnlineSubscription(
                broadcaster_user_id=payload.user_id,
            ),
            eventsub.StreamOfflineSubscription(
                broadcaster_user_id=payload.user_id,
            ),
        ]

        resp: twitchio.MultiSubscribePayload = await self.multi_subscribe(subs)
        if resp.errors:
            LOGGER.warning("Failed to subscribe to: "
                           "%r, for user: %s", resp.errors, payload.user_id)

    async def add_token(self, token: str, refresh: str) \
            -> twitchio.authentication.ValidateTokenPayload:

        resp: twitchio.authentication.ValidateTokenPayload \
            = await super().add_token(token, refresh)

        query = """
        INSERT INTO tokens (user_id, token, refresh)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET
            token = excluded.token,
            refresh = excluded.refresh;
        """

        async with self.token_database.acquire() as connection:
            await connection.execute(query, (resp.user_id, token, refresh))

        LOGGER.info("Added token to the database for user: %s", resp.user_id)
        return resp

    async def event_ready(self) -> None:
        LOGGER.info("Successfully logged in as: %s", self.bot_id)

    async def event_command_error(
        self,
        payload: commands.CommandErrorPayload,
    ) -> None:
        ctx = payload.context
        error = payload.exception

        if isinstance(error, commands.CommandNotFound):
            await ctx.reply(
                f'{ctx.chatter}: Команда "{ctx.invoked_with}" не найдена.'
            )
            return
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(
                f'{ctx.chatter} командой нельзя спамить, подождите {round(error.remaining)} секунд'
            )
            return

        LOGGER.error(
            'Ошибка при выполнении команды "%s":',
            ctx.command,
            exc_info=error,
        )

    async def event_follow(self, payload: twitchio.ChannelFollow) -> None:
        follower_name = payload.user.name
        channel_name = payload.broadcaster.name

        # Печатаем лог в консоль бота
        print(f"[ФОЛЛОУ] Пользователь {follower_name} подписался на канал {channel_name}!")

        # Отправляем приветственное сообщение обратно в чат стримера
        try:
            channel = self.create_partialuser(user_id=self.owner_id)

            await channel.send_message(
                f"Привет, @{follower_name} спасибо за фоллоу! Наш тгк: t.me/pingvinius_228 🎉",
                sender=self.user,  # self.user
            )
        except Exception as e:
            print(f"Не удалось отправить сообщение в чат: {e}")

    async def event_stream_online(self, payload: twitchio.StreamOnline) -> None:
        channel_name = payload.broadcaster.name
        started_at = payload.started_at

        print("Стрим онлайн!")

        try:
            channel = self.create_partialuser(user_id=self.owner_id)

            await channel.send_message(
                f"{channel_name} запустил стрим, время запуска: ({started_at}).",
                sender=self.user,  # self.user
            )
        except Exception as e:
            print(f"Не удалось отправить сообщение в чат: {e}")

    async def event_stream_offline(self, payload: twitchio.StreamOffline) -> None:
        channel_name = payload.broadcaster.name

        print("Стрим оффлайн!")

        try:
            channel = self.create_partialuser(user_id=self.owner_id)

            await channel.send_message(
                f"{channel_name} оффлайн, все новости в нашем тгк: t.me/pingvinius_228",
                sender=self.user,  # self.user
            )
        except Exception as e:
            print(f"Не удалось отправить сообщение в чат: {e}")

    @routines.routine(delta=timedelta(minutes=5))
    async def periodic_message(self):
        channel = self.create_partialuser(user_id=self.owner_id)
        if channel:
            await channel.send_message('Текст вашего периодического сообщения!')
