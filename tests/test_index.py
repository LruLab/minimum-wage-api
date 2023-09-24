from fastapi.testclient import TestClient
from api.index import app

client = TestClient(app)

def test_no_query():
    response = client.get("/")
    assert response.status_code == 200
    assert len(response.json()) == 47

def test_prefecture_query():
    response = client.get("/?prefecture=東京都")
    assert response.status_code == 200
    assert len(response.json()) == 1
    for record in response.json():
        assert record["prefecture"] == "東京"

def test_date_query():
    response = client.get("/?date=2021-01-01")
    assert response.status_code == 200
    assert len(response.json()) == 47
    for record in response.json():
        assert record["date_of_issue"] <= "2021-01-01"    