from fastapi.testclient import TestClient

from backend.app import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_predict():
    response = client.post(
        "/predict",
        json={
            "attendance": 85,
            "internal_marks": 78,
            "assignment_percentage": 90,
            "study_hours": 4,
            "previous_marks": 82,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "prediction" in data
    assert "confidence" in data
    assert "risk_level" in data
    assert "recommendations" in data
    assert "feature_importance" in data


def test_invalid_prediction_input_is_rejected():
    response = client.post(
        "/predict",
        json={
            "attendance": 101,
            "internal_marks": 65,
            "assignment_percentage": 55,
            "study_hours": 3,
            "previous_marks": 80,
        },
    )

    assert response.status_code == 422


def test_feature_importance_endpoint():
    response = client.get("/feature-importance")
    assert response.status_code == 200
    payload = response.json()
    assert "features" in payload
    assert "importances" in payload
    assert len(payload["features"]) == len(payload["importances"])


def test_model_comparison_endpoint():
    response = client.get("/model-comparison")
    assert response.status_code == 200
    payload = response.json()
    assert "models" in payload
    assert len(payload["models"]) >= 2
    assert all("accuracy" in model for model in payload["models"])


def test_prediction_history_endpoint():
    response = client.get("/prediction-history")
    assert response.status_code == 200
    payload = response.json()
    assert "history" in payload