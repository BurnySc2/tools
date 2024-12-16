from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from prisma import Prisma

_db: Prisma | None = None
_lock = asyncio.Lock()


@asynccontextmanager
async def get_db() -> AsyncGenerator[Prisma, None]:
    # https://github.com/RobertCraigie/prisma-client-py/issues/103
    # TODO What if connection is interrupted?
    global _db
    if _db is None:
        async with _lock:
            if _db is None:
                db = Prisma()
                await db.connect()
                _db = db
    yield _db


async def main():
    pass
    # response: APIResponse = await supabase.table(DiscordMessage.table_name()).select("*").limit(10).execute()

    # # for message in DiscordMessage.from_select(response):
    # for row in response.data:
    #     _message = DiscordMessage(**row)
    #     print(row)

    # _messages = DiscordMessage.from_select(response)

    # # End session
    # await supabase.postgrest.aclose()


if __name__ == "__main__":
    asyncio.run(main())
