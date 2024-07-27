from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from main.api.config import settings

from main.api.logger.logger import logger
from main.api.utils.response_util import ok_response

route = settings.route

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(f"{route}")
async def server_liveness():
    """
    Server liveness probe.
    Used by automated tools to check that the server is online.
    """
    return ok_response(message="The Rest server is alive!")


@app.on_event("shutdown")
async def shutdown():
    logger.info("Server is shutting down!")


@app.on_event("startup")
async def startup():
    logger.info("Server is starting up!")
