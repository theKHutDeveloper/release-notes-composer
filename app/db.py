from __future__ import annotations

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .models import Base

_engine = None
_Session = None


def init_db(app: Flask) -> None:
    """Initialise the SQLAchemy engine/session and create tables.
    Call this once during app startup.
    """
    global _engine, _Session
    url = app.config["DATABASE_URL"]
    _engine = create_engine(url, future=True)
    _Session = scoped_session(sessionmaker(bind=_engine, autoflush=False, autocommit=False))

    # ensure a clean schema when running tests
    if app.config.get("TESTING"):
        Base.metadata.drop_all(_engine)
    # Create tables (models import above)
    Base.metadata.create_all(_engine)

    @app.teardown_appcontext
    def _remove_session(_exc):
        # Ensure sessions are cleaned up between requests/CLI runs
        if _Session is not None:
            _Session.remove()


def get_engine():
    if _engine is None:
        raise RuntimeError("DB not initialised. Did you call init_db(app)?")
    return _engine


def get_session():
    if _Session is None:
        raise RuntimeError("DB not initialised. Did you call init_db(app)?")
    return _Session()
