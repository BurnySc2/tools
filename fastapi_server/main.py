import os
from typing import Literal

import uvicorn  # pyre-fixme[21]
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from models.todo_item import create_tables
from routes.chat import chat_router
from routes.hello_world import hello_world_router
from routes.replay_parser import replay_parser_router
from routes.todolist import todo_list_router
from routes.todolist_htmx import htmx_todolist_router
from routes.twitch_clipper import clip_router

assert os.getenv("STAGE", "DEV") in {"DEV", "PROD"}, os.getenv("STAGE")
STAGE: Literal["DEV", "PROD"] = os.getenv("STAGE", "DEV")  # pyre-fixme[9]

app = FastAPI()
app.include_router(hello_world_router)
app.include_router(replay_parser_router)
app.include_router(todo_list_router)
app.include_router(clip_router)
app.include_router(htmx_todolist_router)

origins = [
    "https://burnysc2.github.io",
    "https://replaycomparer.netlify.app",
    "https://burnysc2-monorepo.netlify.app",
    "https://burnysc2-monorepo-dev.netlify.app",
]

logger.info(f"Starting in 'STAGE == {STAGE}' mode")
if STAGE != "PROD":
    origins += [f"http://localhost:{i}" for i in range(1, 2**16)]
    app.include_router(chat_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    # asyncio.create_task(background_task_function('hello', other_text=' world!'))
    await create_tables()
    logger.info("Hello world!")


@app.on_event("shutdown")
def shutdown_event():
    logger.info("Bye world!")


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
