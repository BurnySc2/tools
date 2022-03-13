from pathlib import Path

import uvicorn
from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from fastapi_server.routes.chat import chat_router
from fastapi_server.routes.hello_world import hello_world_router
from fastapi_server.routes.replay_parser import replay_parser_router
from fastapi_server.routes.todolist import todo_list_router

env_path = Path(__file__).parent / '.env'
if not env_path.is_file():
    logger.info(
        """Local .env file in "fastapi_server" directory does not exist. For local development please fill it with contents:
STAGE=dev"""
    )

config: dict = dotenv_values(env_path)

app = FastAPI()
app.include_router(hello_world_router)
app.include_router(replay_parser_router)

origins = ['https://burnysc2.github.io', 'https://replaycomparer.netlify.app']
if config.get('STAGE', '') != 'prod':
    logger.info("Starting in 'STAGE == dev' mode")
    origins += [f'http://localhost:{i}' for i in range(1, 2**16)]
    app.include_router(todo_list_router)
    app.include_router(chat_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def startup_event():
    # asyncio.create_task(background_task_function('hello', other_text=' world!'))
    logger.info('Hello world!')


@app.on_event('shutdown')
def shutdown_event():
    logger.info('Bye world!')


if __name__ == '__main__':
    uvicorn.run('__main__:app', host='0.0.0.0', port=8000, reload=True)
