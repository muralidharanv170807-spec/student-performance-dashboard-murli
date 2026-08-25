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
    assert "reasons" in data
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
    assert set(payload["features"]) == {
        "attendance",
        "internal_marks",
        "assignment_percentage",
        "study_hours",
        "previous_marks",
    }


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


def test_analytics_endpoint():
    response = client.get("/analytics")
    assert response.status_code == 200
    payload = response.json()
    for key in [
        "total_predictions",
        "good_predictions",
        "average_predictions",
        "poor_predictions",
        "at_risk_students",
        "average_attendance",
        "average_marks",
        "average_study_hours",
    ]:
        assert key in payload


def test_what_if_endpoint():
    response = client.post(
        "/what-if",
        json={
            "current": {
                "attendance": 70,
                "internal_marks": 60,
                "assignment_percentage": 50,
                "study_hours": 2,
                "previous_marks": 60,
            },
            "modified": {
                "attendance": 85,
                "internal_marks": 75,
                "assignment_percentage": 80,
                "study_hours": 5,
                "previous_marks": 80,
            },
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert "current" in payload
    assert "modified" in payload
    assert "message" in payload


def test_risk_calculation_rejects_low_for_zero_study_hours():
    response = client.post(
        "/predict",
        json={
            "attendance": 90,
            "internal_marks": 85,
            "assignment_percentage": 92,
            "study_hours": 0,
            "previous_marks": 88,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["risk_level"] != "LOW"
    assert any("study hours" in reason.lower() for reason in payload["reasons"])


def test_clear_prediction_history_endpoint():
    response = client.delete("/prediction-history")
    assert response.status_code == 200
    payload = response.json()
    assert "cleared" in payload["message"].lower()

    analytics = client.get("/analytics")
    assert analytics.status_code == 200
    assert analytics.json()["total_predictions"] == 0