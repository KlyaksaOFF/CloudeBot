import asqlite
from twitchio import eventsub

BOT_ID = "996893706"  # The Account ID of the bot user...


async def setup_database(
    db: asqlite.Pool,
) -> tuple[list[tuple[str, str]], list[eventsub.SubscriptionPayload]]:

    query = """
    CREATE TABLE IF NOT EXISTS tokens(
        user_id TEXT PRIMARY KEY,
        token TEXT NOT NULL,
        refresh TEXT NOT NULL
    )
    """

    async with db.acquire() as connection:
        await connection.execute(query)

        rows = await connection.fetchall("SELECT * FROM tokens")

        tokens: list[tuple[str, str]] = []
        subs: list[eventsub.SubscriptionPayload] = []

        for row in rows:
            tokens.append((row["token"], row["refresh"]))

            subs.append(
                eventsub.ChatMessageSubscription(
                    broadcaster_user_id=row["user_id"],
                    user_id=BOT_ID,
                )
            )

    return tokens, subs