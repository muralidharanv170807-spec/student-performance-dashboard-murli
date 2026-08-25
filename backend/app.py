from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

APP_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = APP_ROOT / "dataset" / "student_performance.csv"
MODEL_PATH = APP_ROOT / "backend" / "model" / "student_model.pkl"
DB_PATH = APP_ROOT / "backend" / "student_performance.db"
FEATURES = [
    "attendance",
    "internal_marks",
    "assignment_percentage",
    "study_hours",
    "previous_marks",
]
TARGET_FIELD = "performance"

RISK_THRESHOLDS = {
    "attendance": 70,
    "internal_marks": 60,
    "assignment_percentage": 60,
    "study_hours": 3,
    "previous_marks": 60,
}


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attendance REAL,
            internal_marks REAL,
            assignment_percentage REAL,
            study_hours REAL,
            previous_marks REAL,
            prediction TEXT,
            confidence REAL,
            risk_level TEXT,
            reasons TEXT,
            recommendations TEXT,
            created_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


model_data = joblib.load(MODEL_PATH)
model = model_data["model"]
label_encoder = model_data["label_encoder"]
features = model_data["features"]


class StudentInput(BaseModel):
    attendance: float = Field(..., ge=0, le=100)
    internal_marks: float = Field(..., ge=0, le=100)
    assignment_percentage: float = Field(..., ge=0, le=100)
    study_hours: float = Field(..., ge=0, le=24)
    previous_marks: float = Field(..., ge=0, le=100)


class WhatIfInput(BaseModel):
    current: StudentInput
    modified: StudentInput


app = FastAPI(
    title="Student Performance Prediction API",
    description="Predictive student performance analytics with risk, recommendations, and comparison tools.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "https://student-performance-cicd-1.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def compute_feature_importance() -> list[dict[str, Any]]:
    importances = model.feature_importances_
    ranked = [
        {
            "feature": feature,
            "importance": round(float(value), 4),
            "label": feature.replace("_", " ").title(),
        }
        for feature, value in zip(features, importances)
    ]
    return sorted(ranked, key=lambda item: item["importance"], reverse=True)


def calculate_risk_level(student_values: dict[str, float], prediction: str) -> tuple[str, list[str]]:
    reasons: list[str] = []

    if student_values["attendance"] < RISK_THRESHOLDS["attendance"]:
        reasons.append("Attendance is below the recommended level.")
    if student_values["internal_marks"] < RISK_THRESHOLDS["internal_marks"]:
        reasons.append("Internal marks are below the expected range.")
    if student_values["assignment_percentage"] < RISK_THRESHOLDS["assignment_percentage"]:
        reasons.append("Assignment performance is below the expected range.")
    if student_values["study_hours"] < RISK_THRESHOLDS["study_hours"]:
        reasons.append("Study hours are below the recommended level.")
    if student_values["previous_marks"] < RISK_THRESHOLDS["previous_marks"]:
        reasons.append("Previous marks indicate weaker academic readiness.")
    if prediction == "Poor":
        reasons.append("The model indicates a likely performance decline.")

    if not reasons:
        return "LOW", []
    if len(reasons) <= 2:
        return "MEDIUM", reasons
    return "HIGH", reasons


def generate_recommendations(student_values: dict[str, float], prediction: str) -> list[str]:
    recommendations: list[str] = []

    if student_values["attendance"] < 75:
        recommendations.append("Improve attendance by attending classes consistently and reducing absenteeism.")
    if student_values["internal_marks"] < 60:
        recommendations.append("Focus more on internal assessments by revising earlier topics and practicing regularly.")
    if student_values["assignment_percentage"] < 60:
        recommendations.append("Complete assignments on time and review the feedback to improve performance.")
    if student_values["study_hours"] < 3:
        recommendations.append("Increase daily study time to strengthen understanding and retention.")
    if student_values["previous_marks"] < 60:
        recommendations.append("Seek academic support and revise previous exam concepts to build confidence.")
    if prediction == "Good" and not recommendations:
        recommendations.append("Maintain the current study routine and keep building on your strengths.")
    if not recommendations:
        recommendations.append("Keep your learning routine steady and continue improving across all academic areas.")

    return recommendations[:4]


def build_prediction_payload(student_values: dict[str, float]) -> dict[str, Any]:
    input_frame = pd.DataFrame([student_values], columns=features)
    prediction_number = model.predict(input_frame)[0]
    prediction = label_encoder.inverse_transform([prediction_number])[0]
    probabilities = model.predict_proba(input_frame)[0]
    confidence = float(max(probabilities))
    risk_level, reasons = calculate_risk_level(student_values, prediction)
    recommendations = generate_recommendations(student_values, prediction)

    return {
        "prediction": prediction,
        "confidence": round(confidence * 100, 2),
        "risk_level": risk_level,
        "reasons": reasons,
        "recommendations": recommendations,
        "feature_importance": compute_feature_importance(),
        "input": student_values,
    }


def record_prediction(student_values: dict[str, float], result: dict[str, Any]) -> None:
    conn = get_db_connection()
    conn.execute(
        """
        INSERT INTO prediction_history (
            attendance, internal_marks, assignment_percentage, study_hours, previous_marks,
            prediction, confidence, risk_level, reasons, recommendations, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            student_values["attendance"],
            student_values["internal_marks"],
            student_values["assignment_percentage"],
            student_values["study_hours"],
            student_values["previous_marks"],
            result["prediction"],
            result["confidence"],
            result["risk_level"],
            json.dumps(result["reasons"]),
            json.dumps(result["recommendations"]),
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    conn.commit()
    conn.close()


def compare_models() -> dict[str, Any]:
    dataset = pd.read_csv(DATA_PATH)
    X = dataset[FEATURES]
    y = dataset[TARGET_FIELD]

    label_encoder_local = LabelEncoder()
    y_encoded = label_encoder_local.fit_transform(y)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=0.2,
        random_state=42,
        stratify=y_encoded,
    )

    model_specs = [
        ("Logistic Regression", LogisticRegression(max_iter=500, random_state=42)),
        ("Decision Tree", DecisionTreeClassifier(random_state=42)),
        ("Random Forest", RandomForestClassifier(n_estimators=200, random_state=42)),
        ("KNN", KNeighborsClassifier(n_neighbors=5)),
        ("SVM", SVC(probability=True, random_state=42)),
    ]

    metrics_list: list[dict[str, Any]] = []
    for model_name, estimator in model_specs:
        estimator.fit(X_train, y_train)
        predictions = estimator.predict(X_test)
        metrics_list.append(
            {
                "model": model_name,
                "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
                "precision": round(float(precision_score(y_test, predictions, average="weighted", zero_division=0)), 4),
                "recall": round(float(recall_score(y_test, predictions, average="weighted", zero_division=0)), 4),
                "f1": round(float(f1_score(y_test, predictions, average="weighted", zero_division=0)), 4),
            }
        )

    best_model = max(metrics_list, key=lambda item: item["f1"])
    return {
        "models": metrics_list,
        "best_model": best_model["model"],
        "best_metric": "F1 Score",
    }


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Student Performance Prediction API is running"}


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "healthy",
        "model_loaded": True,
        "database": str(DB_PATH),
        "features": features,
    }


@app.get("/feature-importance")
def feature_importance() -> dict[str, Any]:
    importance = compute_feature_importance()
    return {
        "features": [item["feature"] for item in importance],
        "importances": [item["importance"] for item in importance],
        "feature_importance": importance,
    }


@app.get("/model-comparison")
def model_comparison() -> dict[str, Any]:
    return compare_models()


@app.get("/prediction-history")
def prediction_history() -> dict[str, Any]:
    conn = get_db_connection()
    rows = conn.execute(
        """
        SELECT id, attendance, internal_marks, assignment_percentage, study_hours, previous_marks,
               prediction, confidence, risk_level, reasons, recommendations, created_at
        FROM prediction_history
        ORDER BY created_at DESC
        """
    ).fetchall()
    conn.close()

    history = []
    for row in rows:
        history.append(
            {
                "id": row["id"],
                "attendance": row["attendance"],
                "internal_marks": row["internal_marks"],
                "assignment_percentage": row["assignment_percentage"],
                "study_hours": row["study_hours"],
                "previous_marks": row["previous_marks"],
                "prediction": row["prediction"],
                "confidence": row["confidence"],
                "risk_level": row["risk_level"],
                "reasons": json.loads(row["reasons"] or "[]"),
                "recommendations": json.loads(row["recommendations"] or "[]"),
                "created_at": row["created_at"],
            }
        )

    return {"history": history}


@app.get("/analytics")
def analytics() -> dict[str, Any]:
    conn = get_db_connection()
    summary = conn.execute(
        """
        SELECT COUNT(*) AS total_predictions,
               SUM(CASE WHEN prediction = 'Good' THEN 1 ELSE 0 END) AS good_count,
               SUM(CASE WHEN prediction = 'Average' THEN 1 ELSE 0 END) AS average_count,
               SUM(CASE WHEN prediction = 'Poor' THEN 1 ELSE 0 END) AS poor_count,
               SUM(CASE WHEN risk_level = 'HIGH' THEN 1 ELSE 0 END) AS high_risk_count,
               AVG(attendance) AS avg_attendance,
               AVG(internal_marks) AS avg_internal_marks,
               AVG(assignment_percentage) AS avg_assignment_percentage,
               AVG(study_hours) AS avg_study_hours,
               AVG(previous_marks) AS avg_previous_marks
        FROM prediction_history
        """
    ).fetchone()
    conn.close()

    if not summary or summary["total_predictions"] == 0:
        return {
            "total_predictions": 0,
            "good_predictions": 0,
            "average_predictions": 0,
            "poor_predictions": 0,
            "at_risk_students": 0,
            "average_attendance": 0,
            "average_marks": 0,
            "average_study_hours": 0,
        }

    return {
        "total_predictions": summary["total_predictions"],
        "good_predictions": summary["good_count"],
        "average_predictions": summary["average_count"],
        "poor_predictions": summary["poor_count"],
        "at_risk_students": summary["high_risk_count"],
        "average_attendance": round(float(summary["avg_attendance"] or 0), 2),
        "average_marks": round(float(((summary["avg_internal_marks"] or 0) + (summary["avg_previous_marks"] or 0)) / 2), 2),
        "average_study_hours": round(float(summary["avg_study_hours"] or 0), 2),
    }


@app.post("/predict")
def predict(student: StudentInput) -> dict[str, Any]:
    student_values = {
        "attendance": student.attendance,
        "internal_marks": student.internal_marks,
        "assignment_percentage": student.assignment_percentage,
        "study_hours": student.study_hours,
        "previous_marks": student.previous_marks,
    }
    result = build_prediction_payload(student_values)
    record_prediction(student_values, result)
    return result


@app.post("/what-if")
def what_if(payload: WhatIfInput) -> dict[str, Any]:
    current_values = {
        "attendance": payload.current.attendance,
        "internal_marks": payload.current.internal_marks,
        "assignment_percentage": payload.current.assignment_percentage,
        "study_hours": payload.current.study_hours,
        "previous_marks": payload.current.previous_marks,
    }
    modified_values = {
        "attendance": payload.modified.attendance,
        "internal_marks": payload.modified.internal_marks,
        "assignment_percentage": payload.modified.assignment_percentage,
        "study_hours": payload.modified.study_hours,
        "previous_marks": payload.modified.previous_marks,
    }

    current_result = build_prediction_payload(current_values)
    modified_result = build_prediction_payload(modified_values)
    difference = current_result["prediction"] + " → " + modified_result["prediction"]

    return {
        "current": current_result,
        "modified": modified_result,
        "difference": difference,
        "prediction_changed": current_result["prediction"] != modified_result["prediction"],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)