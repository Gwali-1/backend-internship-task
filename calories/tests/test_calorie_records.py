from ..main import app
from fastapi.testclient import TestClient


client = TestClient(app)
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNjg3MDMzMDQ4fQ.z2qI4aviC7epbYyhZAAtbzJ4Vg-5ql8FZqyLVeNo6LU"
INVALID_TOKEN=""

def test_get_user_records():
    response = client.get(f"/calories/user_records?token={TOKEN}")
    assert response.status_code == 200
    assert "food_name" in response.json()[0]



def test_get_user_records_invalid_token():
    response = client.get(f"/calories/user_records?token={INVALID_TOKEN}")
    assert response.status_code == 401
    assert response.json() == {"detail":"Could not validate credentials, log in for valid access token"}



def test_add_record():
    response = client.post(f"/calories/add_record?token={TOKEN}", json ={
        "food_name":"rice",
        "calories": 34.8
    })

    assert response.status_code == 200
    assert "id" in response.json()

def test_get_record_by_limit_true():
    response = client.get(f"/calories/get_record_by_limit/true?token={TOKEN}")
    assert response.status_code == 200
    if response.json():
        assert response.json()[0]["below_limit"] == True

def test_get_record_by_limit_false():
    response = client.get(f"/calories/get_record_by_limit/false?token={TOKEN}")
    assert response.status_code == 200
    if response.json():
        assert response.json()[0]["below_limit"] == False



