from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncGenerator, Awaitable, Callable
from pathlib import Path
from typing import Any

import hikari.errors
from dotenv import load_dotenv
from hikari import (
    Embed,
    GatewayBot,
    GuildMessageCreateEvent,
    GuildReactionAddEvent,
    GuildTextChannel,
    Intents,
    Message,
    OwnGuild,
    StartedEvent,
)
from hikari.channels import ChannelType
from loguru import logger

from cache import get_db
from commands.public_fetch_aoe4 import public_analyse_aoe4_game, public_fetch_aoe4_bo, public_search_aoe4_players
from commands.public_leaderboard import public_leaderboard
from commands.public_mmr import public_mmr
from commands.public_remind import Remind
from commands.public_twss import public_twss

load_dotenv()

STAGE = os.getenv("STAGE")
assert STAGE in {"DEV", "PROD"}, STAGE

# pyre-fixme[6]
bot = GatewayBot(token=os.getenv("DISCORD_KEY"), intents=Intents.ALL)
BOT_USER_ID: int = -1

# Discord command prefix
PREFIX = "!"

# Start reminder plugin
my_reminder: Remind = Remind(bot)

# Paths and folders of permanent data
DATA_FOLDER = Path(__file__).parent / "data"
logger.add(DATA_FOLDER / "bot.log")


async def generic_command_caller(
    event: GuildMessageCreateEvent,
    function_to_call: Callable[[GatewayBot, GuildMessageCreateEvent, str], Awaitable[Embed | str]],
    message: str,
    add_remove_emoji: bool = False,
) -> None:
    """
    @param event
    @param function_to_call: A function to be called with the given message,
    expects function to return an Embed or string
    @param message: Parsed messaged by the user, without the command
    @param add_remove_emoji: If true, bot will react to its own message with a 'X' emoji
    so that the mentioned user can remove the bot message at will.
    """
    channel = event.get_channel()
    if not channel:
        return

    # Call the given function with the bot, event and message
    response: Embed | str | None = await function_to_call(bot, event, message)
    if response is None:
        # Function errored or no results
        return

    if isinstance(response, Embed):
        sent_message = await event.message.respond(f"{event.author.mention}", embed=response, reply=False)
    else:
        # Error message or raw string response
        sent_message = await event.message.respond(f"{event.author.mention} {response}", reply=False)
    if add_remove_emoji:
        # https://www.fileformat.info/info/unicode/char/274c/index.htm
        await sent_message.add_reaction("\u274c")


async def loop_function() -> None:
    """A function that is called every X seconds based on the asyncio.sleep(time) below."""
    while 1:
        await asyncio.sleep(1)
        await my_reminder.tick()


async def get_text_channels_of_server(server: OwnGuild) -> AsyncGenerator[GuildTextChannel, None]:
    assert isinstance(server, OwnGuild), type(server)
    for channel in await bot.rest.fetch_guild_channels(server):
        if channel.type not in {ChannelType.GUILD_TEXT}:
            continue
        assert isinstance(channel, GuildTextChannel), type(channel)
        yield channel


async def add_message_to_db(server_id: int, channel_id: int, message: Message) -> None:
    """Insert message into database."""
    if message.content is None:
        return
    async with get_db() as db:
        await db.discordmessage.create(
            data={
                "message_id": message.id,
                "guild_id": server_id,
                "channel_id": channel_id,
                "author_id": message.author.id,
                "who": str(message.author),
                "when": message.created_at,
                "what": message.content,  # TODO Ignore text
            }
        )


async def insert_messages_of_channel_to_db(server: OwnGuild, channel: GuildTextChannel) -> None:
    # Check if bot has access to channel
    if channel.last_message_id is None:
        return
    try:
        _temp_message = await channel.fetch_message(channel.last_message_id)
    except hikari.errors.ForbiddenError:
        logger.error(f"No access to channel '{channel}' in server '{server}'")
        return
    except hikari.errors.NotFoundError:
        logger.error(f"Last message in channel '{channel}' in server '{server}' could not be fetched")
        return

    async with get_db() as db:
        # Grab message ids to not insert duplicates
        messages = await db.query_raw("SELECT message_id FROM discord_message;")
        message_ids: set[int] = {message["message_id"] for message in messages}

    messages_inserted_count = 0
    async for message in channel.fetch_history():
        # Don't process duplicates
        if message.id in message_ids:
            continue
        # Ignore bot and webhook messages
        if message.author.is_bot:
            continue
        # TODO Use bulk insert via List[dict] once API allows it
        # logger.info(f"Inserting message from {message.created_at}")
        await add_message_to_db(server.id, channel.id, message)
        messages_inserted_count += 1
    if messages_inserted_count > 0:
        logger.info(f"Inserted {messages_inserted_count} messages of channel '{channel}' in server '{server}'")


async def get_all_servers() -> AsyncGenerator[OwnGuild, Any]:
    server: OwnGuild
    async for server in bot.rest.fetch_my_guilds():
        yield server
        if STAGE == "PROD":
            # Add all messages to DB
            async for channel in get_text_channels_of_server(server):
                # Create a coroutine that works in background to add messages of specific server and channel to database
                asyncio.create_task(insert_messages_of_channel_to_db(server, channel))


@bot.listen()
async def on_start(_event: StartedEvent) -> None:
    global BOT_USER_ID
    logger.info("Bot started")
    BOT_USER_ID = (await bot.rest.fetch_my_user()).id
    await my_reminder.fetch_next_reminder()
    # Call another async function that runs forever
    asyncio.create_task(loop_function())
    async for server_name in get_all_servers():
        logger.info(f"Connected to server: {server_name}")


@bot.listen()
async def handle_reaction_add(event: GuildReactionAddEvent) -> None:
    if event.member.is_bot:
        return

    channel: GuildTextChannel = await bot.rest.fetch_channel(event.channel_id)  # pyre-fixme[9]
    # Use channel 'bot_tests' only for development
    if STAGE == "DEV" and channel.name != "bot_tests":
        return
    if STAGE == "PROD" and channel.name == "bot_tests":
        return

    message: Message = await bot.rest.fetch_message(event.channel_id, event.message_id)
    if not message:
        return

    # Message is by bot
    # Message has mention
    # Mention is same user who reacted
    # Remove message if :x: was reacted to it
    if (
        message.author.id == BOT_USER_ID
        and message.content
        and f"<@{event.user_id}>" in message.content
        and event.is_for_emoji("\u274c")
    ):
        await message.delete()
        return

    # If "twss" reacted and reaction count >=3: add quote to db
    allowed_emoji_names = {"twss"}
    target_emoji_count = 3
    if STAGE == "DEV" and channel.name == "bot_tests":
        allowed_emoji_names = {"burnysStalker"}
        target_emoji_count = 1
    if not message.author.is_bot and event.emoji_name in allowed_emoji_names:
        for reaction in message.reactions:
            if reaction.emoji.name in allowed_emoji_names and reaction.count >= target_emoji_count:
                # Add quote to db
                if STAGE == "PROD":
                    async with get_db() as db:
                        await db.discordquote.create(
                            data={
                                "message_id": message.id,
                                "guild_id": event.guild_id,
                                "channel_id": event.channel_id,
                                "author_id": message.author.id,
                                "who": str(message.author),
                                "when": message.created_at,
                                "what": message.content,
                                "emoji_name": reaction.emoji.name,
                            }
                        )
                logger.info(f"Added quote: {message.content}")

                # Notify people in channel that a quote has been added
                # TODO and how many there are now in total
                response_message = (
                    f'Added {reaction.emoji.name} quote:\n{message.created_at.strftime("%Y-%m-%d")} '
                    f'{str(message.author)}: {message.content}'
                )
                await channel.send(response_message)
                return


@bot.listen()
async def handle_new_message(event: GuildMessageCreateEvent) -> None:
    """Listen for messages being created."""
    channel = event.get_channel()
    if not channel:
        return
    # Use channel 'bot_tests' only for development
    if STAGE == "DEV" and channel.name != "bot_tests":
        return
    if STAGE == "PROD" and channel.name == "bot_tests":
        return

    # Do not react if messages sent by webhook or bot, or message is empty
    if not event.is_human or not event.content:
        return

    # On new message, add message to DB
    await add_message_to_db(event.guild_id, event.channel_id, event.message)

    # guild = event.get_guild()
    # member = event.get_member()
    #
    # # a = guild.get_emojis()
    # b = await guild.fetch_emojis()
    # animated = next(i for i in b if i.is_animated)

    if event.content is not None and event.content.startswith(PREFIX):
        command, *message_list = event.content.split()
        command = command[len(PREFIX) :]
        message = " ".join(message_list)
        await handle_commands(event, command, message)


async def handle_commands(event: GuildMessageCreateEvent, command: str, message: str) -> None:
    function_mapping = {
        "reminder": my_reminder.public_remind_in,
        "r": my_reminder.public_remind_in,
        "remindat": my_reminder.public_remind_at,
        "ra": my_reminder.public_remind_at,
        "reminders": my_reminder.public_list_reminders,
        "delreminder": my_reminder.public_del_remind,
        "dr": my_reminder.public_del_remind,
        "mmr": public_mmr,
        # "emotes": public_count_emotes,
        "twss": public_twss,
        "leaderboard": public_leaderboard,
        "aoe4find": public_search_aoe4_players,
        "aoe4search": public_search_aoe4_players,
        "aoe4bo": public_fetch_aoe4_bo,
        "aoe4analyse": public_analyse_aoe4_game,
        "aoe4analyze": public_analyse_aoe4_game,
    }
    if command in function_mapping:
        function = function_mapping[command]
        await generic_command_caller(
            event,
            function,
            message,
            add_remove_emoji=True,
        )

    if command == "ping":
        guild = event.get_guild()
        if not guild:
            return
        b = await guild.fetch_emojis()

        animated = next(i for i in b if i.is_animated)
        await event.message.respond(f"Pong! {bot.heartbeat_latency * 1_000:.0f}ms {b[0]} {animated}")


if __name__ == "__main__":
    bot.run()
