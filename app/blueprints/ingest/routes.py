from __future__ import annotations

from flask import Blueprint, jsonify, request
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...db import get_session
from ...models import Change
from ...services.importer_git import parse_git_log

bp = Blueprint("ingest", __name__)


@bp.get("/ping")
def ping():
    return {"ok": True, "service": "ingest"}


@bp.post("")
def ingest():
    """
    Body:
    {
      "source": "git_log",
      "payload": "lines from: git log --date=iso-strict --pretty=format:%H|%an|%ad|%s"
    }
    """
    data = request.get_json(force=True, silent=False)
    source = (data or {}).get("source")
    payload = (data or {}).get("payload", "")

    if source != "git_log":
        return jsonify({"error": "unsupported source"}), 400
    if not payload.strip():
        return jsonify({"error": "payload required"}), 400

    items = parse_git_log(payload)
    sess: Session = get_session()
    created_ids: list[int] = []

    for it in items:
        # de-dupe by commit SHA if present
        if it.get("sha"):
            exists = sess.execute(select(Change.id).where(Change.sha == it["sha"])).first()
            if exists:
                continue

        ch = Change(
            sha=it.get("sha"),
            author=it.get("author"),
            merged_at=it.get("merged_at"),
            title=it.get("title"),
            body=it.get("body"),
        )
        sess.add(ch)
        sess.flush()  # assign id
        created_ids.append(ch.id)

    sess.commit()
    return jsonify({"created": len(created_ids), "ids": created_ids})
