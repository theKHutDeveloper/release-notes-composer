from __future__ import annotations

from flask import Blueprint

bp = Blueprint("releases", __name__)


@bp.get("/ping")
def ping():
    return {"ok": True, "service": "releases"}
