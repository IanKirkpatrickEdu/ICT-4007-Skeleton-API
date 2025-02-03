from fastapi import FastAPI
from loguru import logger

from router.server import api_router
from core.settings import Settings, get_settings

import contextlib
from typing import AsyncGenerator

import fastapi


settings: Settings = get_settings()


@contextlib.asynccontextmanager
async def app_lifespan(_app: fastapi.FastAPI) -> AsyncGenerator:
    """Application lifespan."""
    # Startup commands can go here.
    #   if you need to say connect to a database, do it now
    logger.info("Application Started")
    yield
    # Shutdown commands go here.
    #   if you need to close database connections, do it now
    logger.info("Application Teardown")


def init_app() -> fastapi.FastAPI:
    """Create FastAPI application."""

    server = fastapi.FastAPI(
        title=settings.API_NAME,
        docs_url=settings.SWAGGER_URL,
        redoc_url=settings.REDOC_URL,
        lifespan=app_lifespan,
        # terms_of_service="http://example.com/terms/",
        contact={
            "name": "<YOUR NAME HERE>",
            # "url": "http://ian.kirkpatrick.com",
            "email": "<YOUR EMAIL HERE>",
        },
        license_info={
            "name": "GNU General Public License v3.0",
            "identifier": "GPL-3.0-only",
            "url": "https://www.gnu.org/licenses/gpl-3.0.html",
        }
    )
    server.include_router(api_router)
    return server


app = init_app()