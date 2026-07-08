import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import create_tables
from app.routes import agent_routes, interaction_routes


settings = get_settings()
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interaction_routes.router)
app.include_router(agent_routes.router)


@app.on_event("startup")
def on_startup() -> None:
    try:
        create_tables()
    except Exception as exc:  # pragma: no cover - startup fallback should not block app launch
        logger.warning("Database initialization skipped: %s", exc)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "app": settings.app_name,
        "groq_configured": bool(settings.groq_api_key),
    }
