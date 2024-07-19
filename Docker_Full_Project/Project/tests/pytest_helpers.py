

# pylint: disable = W0613, E0401
import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient

from ValidationStudioCloud.main import app

from ValidationStudioCloud.settings import Settings


def generate_db_instance():
    """To get database details"""
    settings = Settings()
    app.mongodb_client = MongoClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]
    return app.mongodb


@pytest.fixture(name="client")
def fixture_client():
    """Auto build the test client"""
    generate_db_instance()
    var = TestClient(app)
    return var
