import asyncio
import os
import time
from pathlib import Path
from typing import Literal

import uvicorn
from dotenv import load_dotenv
from litestar import Litestar
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig
from loguru import logger

from routes.audiobook.book import MyAudiobookBookRoute
from routes.audiobook.epub_upload import MyAudiobookEpubRoute
from routes.audiobook.index import MyAudiobookIndexRoute
from routes.hello_world import MyRootRoute
from routes.login_logout import MyLoginRoute, MyLogoutRoute
from routes.telegram_browser.telegram_browser import MyTelegramBrowserRoute
from routes.temp_multiswap import MyMultiswapRoute
from routes.text_to_speech import MyTTSRoute
from routes.tts.websocket_handler import TTSWebsocketHandler
from workers.prevent_overflowing_audiobook_bucket import prevent_overflowing_audiobook_bucket

load_dotenv()


assert os.getenv("STAGE", "dev") in {"local_dev", "dev", "prod", "test"}, os.getenv("STAGE")
STAGE: Literal["local_dev", "dev", "prod", "test"] = os.getenv("STAGE")  # pyre-fixme[9]
BACKEND_SERVER_URL = os.getenv("BACKEND_SERVER_URL", "http://localhost:8000")
WS_BACKEND_SERVER_URL = os.getenv("BACKEND_WS_SERVER_URL", "ws:localhost:8000")
logger.info(f"Server url: {BACKEND_SERVER_URL}")
t0 = time.time()


async def startup_event():
    if STAGE == "test":
        return
    # Run websocket handler which handles tts
    # asyncio.create_task(TTSQueue.start_irc_bot())
    # Remove books and minio objects if minio bucket is overflowing
    asyncio.create_task(prevent_overflowing_audiobook_bucket())
    logger.info(f"Startup took {time.time() - t0:.2} seconds")


def shutdown_event():
    logger.info("Bye world!")


app = Litestar(
    route_handlers=[
        MyAudiobookBookRoute,
        MyAudiobookIndexRoute,
        MyAudiobookEpubRoute,
        # MyChatRoute,
        MyLoginRoute,
        MyLogoutRoute,
        MyMultiswapRoute,
        MyRootRoute,
        MyTelegramBrowserRoute,
        # MyTodoRoute,
        MyTTSRoute,
        TTSWebsocketHandler,
        create_static_files_router(path="/static", directories=["src/assets"]),
    ],
    on_startup=[startup_event],
    on_shutdown=[shutdown_event],
    template_config=TemplateConfig(
        directory=Path("src/templates"),
        engine=JinjaTemplateEngine,
    ),
    debug=BACKEND_SERVER_URL == "http://localhost:8000",
)

if __name__ == "__main__":
    uvicorn.run(
        "__main__:app",
        host="localhost",
        port=8000,
        reload_delay=5,
        reload=BACKEND_SERVER_URL == "http://localhost:8000",
    )
