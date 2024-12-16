import asyncio
from pathlib import Path

import arrow
from hikari import GatewayBot, GuildMessageCreateEvent
from loguru import logger

from cache import get_db


async def public_twss(
    _bot: GatewayBot,
    event: GuildMessageCreateEvent,
    _message: str,
):
    # Pick a random quote
    # TODO Allow to pick a quote of a specific user
    quote = await get_random_twss_quote(event.guild_id)
    if quote is None:
        return "Could not find any twss quotes in the database."
    return quote


async def get_random_twss_quote(server_id: int) -> str | None:
    # <YYYY-MM-DD> <Name>: <Message>
    query = """
SELECT * FROM discord_quote
WHERE guild_id = $1
ORDER BY RANDOM()
LIMIT 1;
"""
    async with get_db() as db:
        quote = await db.discordquote.query_first(query, server_id)
        if quote is None:
            return None
    return f'{quote.when.strftime("%Y-%m-%d")} {quote.who}: {quote.what}'


async def main() -> None:
    quote = await get_random_twss_quote(384968030423351298)
    if quote is None:
        logger.info("No quote could be loaded!")
        return
    logger.info(f"Returned quote: {quote}")


async def load_csv_to_postgres() -> None:
    # TODO Upload data to postgres
    path = Path("path_to_file.csv")
    with path.open() as f:
        data = f.readlines()

    # Don't add duplicates
    async with get_db() as db:
        existing_quotes = await db.discordquote.find_many(where={})
        message_ids = {message.message_id for message in existing_quotes}

        for row in data:
            if not row.strip():
                continue
            user_id, messge_id, name, *rest = row.split(",")
            time = rest[-1]
            content = ",".join(rest[:-1])
            user_id = user_id.strip('"')
            messge_id = messge_id.strip('"')
            name = name.strip('"')
            content = content.strip('"')
            time = time.strip("\n").strip('"')
            time_arrow = arrow.get(time)
            # Add quote to db
            if int(messge_id) in message_ids:
                continue

            await db.discordquote.create(
                data={
                    "message_id": messge_id,
                    "guild_id": 447056980960346113,
                    "channel_id": 1037477281200877608,
                    "author_id": user_id,
                    "who": name,
                    "when": time_arrow.datetime,
                    "what": content,
                    "emoji_name": "twss",
                }
            )


if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(load_csv_to_supabase())
