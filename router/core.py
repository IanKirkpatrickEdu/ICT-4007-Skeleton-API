import fastapi
from typing import Literal
import sys
from core.settings import Settings, get_settings
from pydantic import BaseModel, Field

router = fastapi.APIRouter()

class AppBaseRouteSchema(BaseModel):
    """Model for base base route information."""
    name: str | None = Field(default=None, description="API Name")
    description: str | None = Field(default=None, description="API Description")
    version: str | None = Field(default=None, description="API Version")
    swagger_url: str | None = Field(default=None, description="API Swagger Docs URL")
    redoc_url: str | None = Field(default=None, description="API ReDoc URL")
    python_version: str | None = Field(default=None, description="API Python Version")


@router.get("/", tags=["Status"])
async def app_base_route(
    request: fastapi.Request,
    settings: Settings = fastapi.Depends(get_settings),
) -> AppBaseRouteSchema:
    """Root API endpoint, our base route."""
    swagger_docs_url = f"{request.url.scheme}://{request.url.netloc}{settings.SWAGGER_URL}"
    redoc_docs_url = f"{request.url.scheme}://{request.url.netloc}{settings.REDOC_URL}"
    return AppBaseRouteSchema(
        name=settings.API_NAME,
        description=settings.API_DESCRIPTION,
        version=settings.API_VERSION,
        swagger_url=swagger_docs_url,
        redoc_url=redoc_docs_url,
        python_version=sys.version,
    )


@router.get("/health", tags=["Status"])
async def health_check_route() -> Literal["ok"]:
    """Root API endpoint used for health check."""
    return "ok"