import asyncio
import os
from pathlib import Path
from typing import Literal

import uvicorn
from dotenv import load_dotenv
from litestar import Litestar, MediaType, get
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig
from loguru import logger

from routes.audiobook.from_epub import MyAudiobookEpubRoute, background_convert_function
from routes.hello_world import MyRootRoute
from routes.htmx_chat import MyChatRoute
from routes.htmx_todolist import MyTodoRoute
from routes.login_logout import MyLoginRoute, MyLogoutRoute

# from routes.similar_words import MyWordsRoute
from routes.text_to_speech import MyTTSRoute
from routes.tts.websocket_handler import TTSQueue, TTSWebsocketHandler

load_dotenv()


# Paths and folders of permanent data
DATA_FOLDER = Path(__file__).parent / "data"
logger.add(DATA_FOLDER / "app.log")

assert os.getenv("STAGE", "dev") in {"dev", "prod"}, os.getenv("STAGE")
STAGE: Literal["dev", "prod"] = os.getenv("STAGE", "dev")  # pyre-fixme[9]
BACKEND_SERVER_URL = os.getenv("BACKEND_SERVER_URL", "0.0.0.0:8000")
WS_BACKEND_SERVER_URL = os.getenv("BACKEND_WS_SERVER_URL", "ws:0.0.0.0:8000")


@get(path="/", media_type=MediaType.TEXT)
async def index() -> str:
    return "Hello, world!"


@get("/books/{book_id:int}")
async def get_book(book_id: int) -> dict[str, int]:
    return {"book_id": book_id}


async def startup_event():
    # Run websocket handler which handles tts
    asyncio.create_task(TTSQueue.start_irc_bot())
    asyncio.create_task(background_convert_function())

    # asyncio.create_task(background_task_function('hello', other_text=' world!'))
    try:
        # await todo_create_tables()
        # await chat_create_tables()
        pass
    except ConnectionRefusedError:
        logger.error("Is postgres running?")
    logger.info("Started!")


def shutdown_event():
    logger.info("Bye world!")


app = Litestar(
    route_handlers=[
        get_book,
        index,
        MyAudiobookEpubRoute,
        MyChatRoute,
        MyLoginRoute,
        MyLogoutRoute,
        MyRootRoute,
        MyTodoRoute,
        MyTTSRoute,
        TTSWebsocketHandler,
        create_static_files_router(path="/static", directories=["assets"]),
    ],
    on_startup=[startup_event],
    on_shutdown=[shutdown_event],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
    debug=BACKEND_SERVER_URL == "0.0.0.0:8000",
)

if __name__ == "__main__":
    uvicorn.run(
        "__main__:app",
        host="0.0.0.0",
        port=8000,
        reload_delay=5,
        reload=BACKEND_SERVER_URL == "0.0.0.0:8000",
    )
