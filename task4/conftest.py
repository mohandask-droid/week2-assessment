import os

os.environ["DB_NAME"] = "customer_api_test_db"
os.environ["API_KEY"] = "test-key"
os.environ["WEBHOOK_SECRET"] = "test-secret"

import pytest
from fastapi.testclient import TestClient

from database import Base, engine
from main import app


@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def headers():
    return {"X-API-Key": "test-key"}