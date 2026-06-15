"""FastAPI application entrypoint."""

from fastapi import FastAPI
from pydantic import BaseModel

from src.adapters.http.admin_routes import router as admin_router
from src.adapters.http.auth_routes import router as auth_router
from src.adapters.http.order_routes import router as order_router
from src.adapters.websocket.realtime_routes import router as realtime_router
from src.infrastructure.settings import get_settings


class HealthResponse(BaseModel):
    """Health check response contract."""

    status: str
    service: str
    version: str


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.api_version)
    app.include_router(auth_router)
    app.include_router(admin_router)
    app.include_router(order_router)
    app.include_router(realtime_router)

    @app.get("/health", response_model=HealthResponse, tags=["system"])
    async def health() -> HealthResponse:
        """Return service health without touching external dependencies."""

        return HealthResponse(
            status="ok",
            service=settings.app_name,
            version=settings.api_version,
        )

    return app


app = create_app()
