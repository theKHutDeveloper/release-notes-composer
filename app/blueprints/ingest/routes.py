from __future__ import annotations

from flask import Blueprint

bp = Blueprint("ingest", __name__)


@bp.get("/ping")
def ping():
    return {"ok": True, "service": "ingest"}
