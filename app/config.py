from __future__ import annotations

import os


def load_config() -> dict[str, object]:
    """Project settings loaded from environment variables with defaults"""
    return {
        "SECRET_KEY": os.getenv("SECRET_KEY", "dev-secret"),
        "DATABASE_URL": os.getenv("DATABASE_URL", "sqlite:///composer.db"),
        "SITE_TITLE": os.getenv("SITE_TITLE", "Release Notes Composer"),
    }
