import logging
import os

import uvicorn
from fastapi import FastAPI

from controller import router


app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    if os.getenv("PERFORMANCE_TEST") == "true":
        logging.info("Performance testing enabled")
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
