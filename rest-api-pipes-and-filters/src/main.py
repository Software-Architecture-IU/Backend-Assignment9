from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from multiprocessing import Queue
from filters.filter import Filter
from filters.screamer import Screamer
from filters.publisher import Publisher
from filters.base import BaseFilter

from controller import router

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


app = FastAPI(lifespan=prepare_filters)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
