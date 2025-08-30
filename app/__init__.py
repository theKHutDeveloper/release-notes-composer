from __future__ import annotations

from flask import Flask

from .blueprints.classify.routes import bp as classify_bp
from .blueprints.ingest.routes import bp as ingest_bp
from .blueprints.releases.routes import bp as releases_bp
from .blueprints.site.routes import bp as site_bp
from .config import load_config
from .db import init_db


def create_app() -> Flask:
    app = Flask(__name__)

    # load env-driven settings
    app.config.from_mapping(load_config())

    # initialise database (engine, session and create tables)
    init_db(app)

    # Register API blueprints under /api/*
    app.register_blueprint(ingest_bp, url_prefix="/api/ingest")
    app.register_blueprint(classify_bp, url_prefix="/api/classify")
    app.register_blueprint(releases_bp, url_prefix="/api/releases")

    # Site blueprint (no prefix for future pages)
    app.register_blueprint(site_bp)

    @app.get("/")
    def root():
        # simple JSON response
        return {"status": "ok"}

    return app
