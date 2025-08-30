from __future__ import annotations

from flask import Flask

from .config import load_config
from .db import init_db


def create_app() -> Flask:
    app = Flask(__name__)

    # load env-driven settings
    app.config.from_mapping(load_config())

    # initialise database (engine, session and create tables)
    init_db(app)

    @app.get("/")
    def root():
        # simple JSON response
        return {"status": "ok"}

    return app
