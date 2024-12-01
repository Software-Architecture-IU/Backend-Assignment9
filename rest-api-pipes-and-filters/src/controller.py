from fastapi import APIRouter, HTTPException
from schemas import PostUserMessage

from contextlib import asynccontextmanager
from fastapi import FastAPI
from multiprocessing import Queue
from filters.filter import Filter
from filters.screamer import Screamer
from filters.publisher import Publisher
from filters.base import BaseFilter


g_Processes: tuple[BaseFilter]


@asynccontextmanager
async def prepare_filters(app: FastAPI):
    global g_Processes

    filter_input = Queue()
    screamer_input = Queue()
    publisher_input = Queue()

    filter = Filter(filter_input, outputs=[screamer_input])
    screamer = Screamer(screamer_input, outputs=[publisher_input])
    publisher = Publisher(publisher_input)

    g_Processes = (filter, screamer, publisher)
    for process in g_Processes:
        process.start()

    # when it reaches this it stops.
    yield  # when app terminates it executes code after it

    for process in g_Processes:
        process.kill()


router = APIRouter(prefix="", lifespan=prepare_filters)


@router.post("/message")
async def post_message(body: PostUserMessage) -> None:
    global g_Processes
    username = body.user_alias
    msg = body.message

    if is_empty(username):
        raise HTTPException(404, f'User {username} not found')

    if is_empty(msg):
        raise HTTPException(404, f'Message {msg} not found')

    g_Processes[0].input.put(body)


def is_empty(string: str) -> bool:
    return string == '' or string is None
