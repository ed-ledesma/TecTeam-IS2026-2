import os
import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

os.environ.setdefault("PYTHON_DOTENV_DISABLED", "1")
os.environ.setdefault("USERNAME", "test")
os.environ.setdefault("PASSWORD", "test")
os.environ.setdefault("HOST", "localhost")
os.environ.setdefault("PORT", "3306")
os.environ.setdefault("DATABASE", "sgci_test")
os.environ.setdefault("SECRET_KEY", "testing-secret-key")

from app import create_app
from models import db
from tests.factories import crear_idioma


@pytest.fixture()
def app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": "testing-secret-key",
        }
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def idioma():
    idioma = crear_idioma("Inglés")
    db.session.commit()
    return idioma
