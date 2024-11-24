import threading

import uvicorn
from fastapi import FastAPI

from controller import router
from rabbitmq import rabbitmq_producer


def start_heartbeat():
    rabbitmq_producer.send_heartbeat()
    threading.Timer(10, start_heartbeat).start()


app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    start_heartbeat()
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
