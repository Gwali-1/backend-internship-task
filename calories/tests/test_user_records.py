from ..main import app
from fastapi.testclient import TestClient


client = TestClient(app)
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNjg3MDMxOTY4fQ.1EMLUkNhRdBvzX92ijzSuD19ZYGXRoQUVXw0icXPE9Y"
INVALID_TOKEN=""
ROLE="Manager"

def test_get_users_not_authorized():
    response = client.get(f"/users/get_users?token={TOKEN}")
    assert response.status_code == 401




def test_get_users_invalid_token():
    response = client.get(f"/users/get_users?token={INVALID_TOKEN}")
    assert response.status_code == 401




def test_get_users_by_role_not_authorized():
    response = client.get(f"/users/get_users_by_role/{ROLE}?token={TOKEN}")
    assert response.status_code == 401

def test_change_role_not_authorized():
    response = client.put(f"/users/change_role?token={TOKEN}", json={"user_id":3, "role":"Manager"})
    assert response.status_code == 401




