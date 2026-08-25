# Student Performance Prediction Dashboard

A full-stack project that predicts student academic performance using a trained Random Forest model, FastAPI, and a React dashboard.

## Project Description

This project helps identify likely student outcomes, flag early warning risk signals, and show actionable recommendations through a clean analytics dashboard. It combines a trained model, a backend API, a SQLite database, and a responsive frontend.

## Features

- Student performance prediction for Good, Average, and Poor outcomes
- Confidence score from model probability
- Risk assessment and personalized recommendations
- Feature importance visualization from the trained model
- What-if comparison workflow
- Prediction history stored in SQLite
- Analytics summary for historical predictions
- Downloadable plain-text student report
- Responsive dashboard UI
- GitHub Actions CI checks
- Docker support

## Technology Stack

- Python
- FastAPI
- Pydantic
- SQLite
- scikit-learn
- pandas
- joblib
- React
- Vite
- Docker
- GitHub Actions
- Pytest

## Project Structure

```text
student-performance-cicd-starter/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── model/
│   │   └── student_model.pkl
│   ├── tests/
│   │   └── test_api.py
│   └── student_performance.db
├── dataset/
│   └── student_performance.csv
├── frontend/
│   ├── index.html
│   ├── package.json
│   └── src/
│       ├── main.jsx
│       └── style.css
├── ml/
│   ├── preprocessing.py
│   └── train.py
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── README.md
└── .gitignore
```

## Dataset Details

The dataset is located at [dataset/student_performance.csv](dataset/student_performance.csv).

It contains the following fields:

- attendance
- internal_marks
- assignment_percentage
- study_hours
- previous_marks
- performance

The model predicts the categorical label in `performance`:

- Good
- Average
- Poor

## ML Model Details

The project uses a Random Forest classifier trained on the student performance dataset.

The model is trained in [ml/train.py](ml/train.py) and saved to:

```text
backend/model/student_model.pkl
```

The model uses these input features:

- attendance
- internal_marks
- assignment_percentage
- study_hours
- previous_marks

The trained pipeline stores:

- the model object
- the label encoder
- the feature list

## Backend Setup

### 1. Create a virtual environment

```bash
python -m venv venv
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Start the FastAPI backend

From the project root:

```bash
uvicorn backend.app:app --reload
```

The API will be available at:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## Frontend Setup

### 1. Install frontend dependencies

```bash
cd frontend
npm install
```

### 2. Run the React/Vite frontend

```bash
npm run dev
```

The app is available at:

- http://localhost:5173

## Environment Variable Configuration

The frontend supports a configurable API base URL:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000
```

If not set, it defaults to:

```text
http://127.0.0.1:8000
```

## How to Train the Model

Run:

```bash
python ml/train.py
```

This trains the Random Forest model and saves the model bundle to the backend model directory.

## API Endpoints

### GET /
Returns a basic service status message.

### GET /health
Returns health information and model status.

### POST /predict
Predicts a student's performance and stores the record in SQLite prediction history.

Request body example:

```json
{
  "attendance": 85,
  "internal_marks": 78,
  "assignment_percentage": 90,
  "study_hours": 4,
  "previous_marks": 82
}
```

Response example:

```json
{
  "prediction": "Good",
  "confidence": 66.0,
  "risk_level": "LOW",
  "reasons": [],
  "recommendations": ["Keep your learning routine steady and continue improving across all academic areas."],
  "feature_importance": [
    {
      "feature": "study_hours",
      "importance": 0.35,
      "label": "Study Hours"
    }
  ]
}
```

### GET /feature-importance
Returns the feature importance rankings from the trained model.

### GET /model-comparison
Returns model comparison metrics for multiple classifiers trained on the dataset.

### GET /prediction-history
Returns the stored prediction history records from SQLite.

### GET /analytics
Returns aggregate analytics based on the actual database contents.

### POST /what-if
Compares the current input profile to a modified profile and shows how the prediction changes.

### DELETE /prediction-history
Clears the prediction history. This is intended for local development and testing.

## Prediction Flow

1. The frontend collects student metrics.
2. The frontend sends a POST request to `/predict`.
3. The backend validates input values.
4. The backend loads the saved ML model.
5. The backend predicts a label using the trained Random Forest model.
6. The backend computes confidence from the model probability.
7. The backend calculates risk level and recommendations.
8. The backend stores the result in SQLite.
9. The frontend displays the exact response from the backend.

## Risk Calculation

The backend computes risk based on the input values and the predicted label.

Important behavior:

- `study_hours <= 0` is treated as a serious risk condition.
- Low attendance, low internal marks, weak assignment performance, and low previous marks add risk reasons.
- The risk result can be LOW, MEDIUM, or HIGH.
- MEDIUM and HIGH are included in At-Risk Students analytics.

## Analytics

Analytics are calculated from actual rows stored in the SQLite database.

The `/analytics` endpoint returns:

- total_predictions
- good_predictions
- average_predictions
- poor_predictions
- at_risk_students
- average_attendance
- average_marks
- average_study_hours

## What-If Analysis

The `/what-if` endpoint compares two student profiles:

- current
- modified

It returns both predictions, confidence values, a message describing the changed outcome, and the prediction delta.

## Prediction History

Prediction results are stored in SQLite using the `prediction_history` table. The app stores:

- attendance
- internal_marks
- assignment_percentage
- study_hours
- previous_marks
- prediction
- confidence
- risk_level
- reasons
- recommendations
- created_at

## Testing

Run the backend test suite:

```bash
.\venv\Scripts\python.exe -m pytest -q
```

The project includes tests for:

- home endpoint
- health endpoint
- prediction endpoint
- invalid input rejection
- feature importance endpoint
- model comparison endpoint
- prediction history endpoint
- analytics endpoint
- what-if endpoint
- risk logic
- history reset behavior

## Production Frontend Build

Run:

```bash
cd frontend
npm run build
```

This produces a production bundle in the `frontend/dist` directory.

## Docker Instructions

The repository includes a `Dockerfile` and `docker-compose.yml`.

Build the backend image:

```bash
docker build -t student-performance-api .
```

Run the container:

```bash
docker run -d --name student-performance-container -p 8000:8000 student-performance-api
```

Or use Docker Compose:

```bash
docker-compose up --build
```

## CI/CD

The project includes GitHub Actions workflow automation in:

```text
.github/workflows/ci-cd.yml
```

The workflow runs:

- backend dependency install
- backend tests
- frontend dependency install
- frontend production build
- Docker image build

## Notes

- The prediction logic is driven by the actual trained model.
- Risk thresholds and recommendations are handled in the backend.
- Analytics and history are based on the real SQLite database records.
- The frontend shows the exact response returned by the backend prediction API.
