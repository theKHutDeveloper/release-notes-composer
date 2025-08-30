import os
import sys

import pytest

# ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import create_app


@pytest.fixture
def app(tmp_path):
    # unique DB path for this test run
    db_path = tmp_path / "test.db"
    app = create_app(
        {
            "TESTING": True,
            "DATABASE_URL": f"sqlite:///{db_path}",
        }
    )
    yield app


@pytest.fixture
def client(app):
    return app.test_client()
