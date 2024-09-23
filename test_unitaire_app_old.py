import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"health_check": "ok", "model_version": "1.0.0"}

def test_predict_positive():
    response = client.post("/predict", json={"text": "I love this service!"})
    assert response.status_code == 200
    assert response.json() == {"prediction": "tweet_positif"}

def test_predict_negative():
    response = client.post("/predict", json={"text": "I hate this service!"})
    assert response.status_code == 200
    assert response.json() == {"prediction": "tweet_négatif"}