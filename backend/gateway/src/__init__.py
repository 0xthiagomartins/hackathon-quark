from fastapi import FastAPI
from . import settings
from .const import TAGS_METADATA
from .routes import (
    auth_router,
    user_router,
    operation_router,
    client_router,
)

from nameko import config

config_setup = {"AMQP_URI": f"{settings.CLOUD_AMQP}"}
config.setup(config_setup)
print(config_setup)
# verify if config.setup worked
print(settings.CLOUD_AMQP)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Quark Investimentos API",
        version="0.0.1",
        openapi_url=settings.OPEN_API_PATH,
        openapi_tags=TAGS_METADATA,
    )
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(operation_router)
    app.include_router(client_router)
    return app
