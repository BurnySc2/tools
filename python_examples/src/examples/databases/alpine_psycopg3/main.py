import asyncio
import os
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import psycopg
from psycopg.rows import dict_row


@asynccontextmanager
async def get_db() -> AsyncGenerator[psycopg.Connection, None]:
    assert os.getenv("POSTGRES_CONNECTION_STRING") is not None
    async with await psycopg.AsyncConnection.connect(os.getenv("POSTGRES_CONNECTION_STRING")) as conn:
        yield conn


async def main():
    t1 = time.time()
    async with get_db() as db:
        t2 = time.time()
        cursor: psycopg.AsyncCursor
        async with db.cursor(row_factory=dict_row) as cursor:
            query = await cursor.execute(
                """
SELECT id, twitch_name
FROM stream_announcer_streams
WHERE id = ANY(%s)
                """,
                [[2, 3]],
            )
            results = await query.fetchall()
        t3 = time.time()
        print(t2 - t1)
        print(t3 - t2)
        print(results)
        return results


if __name__ == "__main__":
    asyncio.run(main())
