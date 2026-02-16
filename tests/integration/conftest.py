import os
import time
import pytest
import psycopg
from fastapi.testclient import TestClient

from app.core.config import settings

def wait_for_db(host, port, dbname, user, password, timeout_s=30):
    start = time.time()
    while True:
        try:
            with psycopg.connect(
                host=host, port=port, dbname=dbname, user=user, password=password,
                connect_timeout=2
            ):
                return
        except Exception:
            if time.time() - start > timeout_s:
                raise
            time.sleep(1)

@pytest.fixture()
def integration_client():
    settings.DB_HOST = os.getenv("TEST_DB_HOST", "localhost")
    settings.DB_PORT = int(os.getenv("TEST_DB_PORT", "55432"))
    settings.DB_NAME = os.getenv("TEST_DB_NAME", "testdb")
    settings.DB_USER = os.getenv("TEST_DB_USER", "test")
    settings.DB_PASSWORD = os.getenv("TEST_DB_PASSWORD", "test123")

    wait_for_db(settings.DB_HOST, settings.DB_PORT, settings.DB_NAME, settings.DB_USER, settings.DB_PASSWORD)

    from app.main import app
    with TestClient(app) as c:
        yield c
