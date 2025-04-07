from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_sales_coupon():
    response = client.post("/api/v1/sales/", json={
        "code": "SALE2024",
        "merchant": "Test Store",
        "discount_percent": 15.5,
        "valid_until": "2024-12-31T23:59:59"
    })
    assert response.status_code == 201
    assert response.json()["code"] == "SALE2024"