from __future__ import annotations

import os
from typing import Literal

# import asyncpg
# from asyncpg import Record

assert os.getenv("STAGE", "dev") in {"dev", "prod"}, os.getenv("STAGE")
STAGE: Literal["dev", "prod"] = os.getenv("STAGE", "dev")  # pyre-fixme[9]

TABLE_NAME = f"{STAGE}_todo_items"


# async def create_connection() -> asyncpg.Connection:
#     # TODO use 'with' statement of possible
#     return await asyncpg.connect(
#         os.getenv("POSTGRES_CONNECTION_STRING"),
#         timeout=60,  # Allow max 60 seconds per connection
#     )


# async def table_exists(table_name: str) -> bool:
#     conn = await create_connection()
#     data: Record = await conn.fetchrow(
#         """
# SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name ILIKE $1);
# """,
#         table_name,
#     )
#     return data.get("exists")


# async def todo_create_tables() -> None:
#     if not await table_exists(TABLE_NAME):
#         conn = await create_connection()
#         async with conn.transaction():
#             await conn.execute(
#                 f"""
# CREATE TABLE {TABLE_NAME} (
# id serial PRIMARY KEY,
# todotext text NOT NULL,
# done boolean NOT NULL
# );
# """
#             )


# async def get_all_todos() -> list[Record]:
#     conn = await create_connection()
#     async with conn.transaction():
#         return await conn.fetch(
#             f"""
# SELECT id, todotext, done FROM {TABLE_NAME}
# ORDER BY id ASC;
# """
#         )


# async def add_todo(todotext: str) -> Record:
#     conn = await create_connection()
#     async with conn.transaction():
#         await conn.execute(
#             f"""
# INSERT INTO {TABLE_NAME} (todotext, done) VALUES ($1, false);
# """,
#             todotext,
#         )
#         # Assume increasing ids
#         row: Record = await conn.fetchrow(
#             f"""
# SELECT id, todotext, done FROM {TABLE_NAME}
# ORDER BY id DESC
# LIMIT 1;
# """
#         )
#         assert row.get("todotext") == todotext
#         return row


# async def toggle_todo(todoid: int) -> None:
#     conn = await create_connection()
#     async with conn.transaction():
#         await conn.execute(
#             f"""
# UPDATE {TABLE_NAME} SET done = NOT done WHERE id = $1;
# """,
#             todoid,
#         )


# async def delete_todo(todoid: int) -> None:
#     conn = await create_connection()
#     async with conn.transaction():
#         await conn.execute(
#             f"""
# DELETE FROM {TABLE_NAME} WHERE id = $1;
# """,
#             todoid,
#         )


# async def main():
#     await todo_create_tables()
#     print(await get_all_todos())


# if __name__ == "__main__":
#     asyncio.run(main())
