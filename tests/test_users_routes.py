from datetime import datetime

def test_list_users_returns_items(client, monkeypatch):
    # Mock del service usado en el router
    from app.api.routes import users as users_route

    class FakeService:
        def list_users(self, limit: int, offset: int):
            return {
                "count": 1,
                "items": [
                    {
                        "id": 1,
                        "first_name": "Alito",
                        "last_name": "Salas",
                        "email": "alito@test.com",
                        "is_active": True,
                        "created_at": datetime.utcnow().isoformat(),
                    }
                ],
            }

    monkeypatch.setattr(users_route, "service", FakeService())

    r = client.get("/users?limit=50&offset=0")
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 1
    assert body["items"][0]["email"] == "alito@test.com"


def test_get_user_404(client, monkeypatch):
    from app.api.routes import users as users_route
    from fastapi import HTTPException

    class FakeService:
        def get_user(self, user_id: int):
            raise HTTPException(status_code=404, detail="User not found")

    monkeypatch.setattr(users_route, "service", FakeService())

    r = client.get("/users/999")
    assert r.status_code == 404
    assert r.json()["detail"] == "User not found"
