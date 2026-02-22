import pytest

pytestmark = pytest.mark.integration


def test_health_ok(integration_client):
    r = integration_client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_list_users_hits_real_db(integration_client):
    r = integration_client.get("/users?limit=50&offset=0")
    assert r.status_code == 200
    body = r.json()

    assert body["count"] >= 2
    emails = [u["email"] for u in body["items"]]
    assert "alito@test.com" in emails
    assert "ana@test.com" in emails


def test_get_user_1_hits_real_db(integration_client):
    r = integration_client.get("/users/1")
    assert r.status_code == 200
    user = r.json()
    assert user["id"] == 1
    assert user["email"] == "alito@test.com"


def test_get_user_404_real_db(integration_client):
    r = integration_client.get("/users/999999")
    assert r.status_code == 404
    assert r.json()["detail"] == "User not found"
