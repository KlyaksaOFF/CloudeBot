import asyncio
import os

import twitchio
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')


async def main() -> None:
    async with twitchio.Client(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET) as client:
        await client.login()
        user = await client.fetch_users(logins=["Clouder_7", "KlyaksaOFF"])
        for u in user:
            print(f"User: {u.name} - ID: {u.id}")


if __name__ == "__main__":
    asyncio.run(main())