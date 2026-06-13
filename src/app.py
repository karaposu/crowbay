# filepath: src/app.py

import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.middleware.base import BaseHTTPMiddleware

from config import settings


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
    )


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title="Crowdjump API",
        description="Launch a task. The crowd jumps on it.",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )
    app.add_middleware(RequestIDMiddleware)

    from routers import auth as auth_router
    from routers import health as health_router
    from routers import phone as phone_router
    from routers import tasks as tasks_router
    from routers import users as users_router

    app.include_router(health_router.router)
    app.include_router(auth_router.router)
    app.include_router(phone_router.router)
    app.include_router(users_router.router)
    app.include_router(tasks_router.router)

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        # e.g. two concurrent jumps racing past the duplicate check into the
        # unique (task_id, jumper_id) constraint.
        return JSONResponse(status_code=409, content={"detail": "Conflict"})

    return app


app = create_app()
