from sqlalchemy import inspect

from app import create_app
from app.db import get_engine


def test_tables_exist():
    create_app()
    engine = get_engine()
    insp = inspect(engine)
    assert insp.has_table("releases")
    assert insp.has_table("changes")
