from collections.abc import Generator
from pathlib import Path
import warnings

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


settings = get_settings()


def _database_url() -> str:
    if not settings.database_url:
        fallback_path = Path(__file__).resolve().parent.parent / "app.db"
        fallback_url = f"sqlite:///{fallback_path.as_posix()}"
        warnings.warn(
            "DATABASE_URL is not configured. Falling back to local SQLite at "
            f"{fallback_path}. Set DATABASE_URL in backend/.env to use Neon PostgreSQL.",
            RuntimeWarning,
        )
        return fallback_url
    return settings.database_url


def _engine_options(database_url: str) -> dict:
    url = make_url(database_url)
    if url.drivername.startswith("sqlite"):
        return {"connect_args": {"check_same_thread": False}}

    options = {"pool_pre_ping": True, "pool_recycle": 300}
    if url.drivername.startswith("postgresql") and "neon.tech" in (url.host or "") and "sslmode" not in url.query:
        options["connect_args"] = {"sslmode": "require"}
    return options


database_url = _database_url()
engine = create_engine(database_url, **_engine_options(database_url))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    from app.models.interaction import Interaction

    Base.metadata.create_all(bind=engine)
