from __future__ import annotations

from flask import Blueprint

bp = Blueprint("classify", __name__)


@bp.get("/ping")
def ping():
    return {"ok": True, "service": "classify"}
