from ..main import app
from fastapi.testclient import TestClient
import string
import random

client = TestClient(app)
res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=5))


def test_create_account():
    response = client.post("/auth/create", json={
        "username":res,
        "password":"password",
        "limit": 34.3
    })

    assert response.status_code == 200


def test_create_account_wrong_payload():
    response = client.post("/auth/create", json={
        "username":"wrong",
        "password":"password",
    })

    assert response.status_code == 422




def test_login():
    response = client.post("/auth/login", data={
        "username":res,
        "password":"password",
    })

    assert response.status_code == 200


def test_login_wrong_credentials():
    response = client.post("/auth/login", data={
        "username":"wrong",
        "password":"password",
    })

    assert response.status_code == 401






