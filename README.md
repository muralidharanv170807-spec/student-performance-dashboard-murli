<<<<<<< HEAD
# 🤖 AI-Based Student Performance Prediction System
=======
# Student Performance Prediction System
>>>>>>> bdcb0f4 (Update student performance application)

A full-stack machine learning project for predicting student academic performance, monitoring risk, and presenting actionable analytics through a responsive dashboard.

<<<<<<< HEAD
An end-to-end **AI and DevOps project** that predicts student academic performance using a machine learning model and automatically delivers the application through a **CI/CD pipeline** using GitHub Actions, Docker, and Render.
=======
## Problem Statement
>>>>>>> bdcb0f4 (Update student performance application)

Educational institutions need a quick way to identify students who may need support before academic performance declines. This project combines a trained classification model, API services, dashboard analytics, and reliable CI checks to help instructors and students evaluate performance and act early.

<<<<<<< HEAD
## 🌐 Live Demo

### Frontend
https://student-performance-cicd-1.onrender.com

### Backend API
https://student-performance-cicd.onrender.com

### API Documentation
https://student-performance-cicd.onrender.com/docs

### Health Check
https://student-performance-cicd.onrender.com/health

---

## 📌 Project Overview

The **AI-Based Student Performance Prediction System** is a web-based machine learning application that predicts a student's academic performance from five input features.

### User Inputs

- Attendance Percentage
- Internal Marks
- Assignment Percentage
- Study Hours per Day
- Previous Marks

### Prediction

The machine learning model predicts:

- **Good**
- **Average**
- **Poor**

The application also displays the model's prediction confidence.

---

## 🎯 Objectives

The main objectives of this project are:

1. Develop a machine learning model for student performance prediction.
2. Build a REST API using FastAPI.
3. Develop a React-based frontend.
4. Connect the frontend with the machine learning API.
5. Containerize the backend using Docker.
6. Create automated tests using Pytest.
7. Implement Continuous Integration using GitHub Actions.
8. Implement Continuous Deployment using Render.
9. Deploy the complete application publicly.

---

## 🏗️ System Architecture

```mermaid
flowchart LR
    A[Developer] --> B[GitHub Repository]
    B --> C[GitHub Actions]
    C --> D[Pytest]
    D --> E[Docker Build]
    E --> F[Render]

    U[User] --> G[React Frontend]
    F --> H[FastAPI Backend]
    G --> H
    H --> I[Random Forest ML Model]
    I --> J[Prediction + Confidence]
    J --> G
=======
## Objectives

- Predict student performance using real academic features.
- Keep the existing model and API behavior compatible while extending the system.
- Add early warning signals and personalized guidance.
- Show feature importance from the actual trained model.
- Compare multiple ML algorithms using real metrics.
- Store prediction history in SQLite for dashboard analytics.
- Validate the system with automated backend tests and frontend builds.

## Technologies Used

- Python
- FastAPI
- Pydantic
- SQLite
- Scikit-learn
- Pandas
- Joblib
- React
- Vite
- Docker
- GitHub Actions
- Pytest

## System Architecture

```mermaid
flowchart LR
    U[Student / Instructor] --> F[React Frontend]
    F --> A[FastAPI Backend]
    A --> DB[(SQLite Database)]
    A --> M[Random Forest Model]
    M --> R[Prediction + Risk + Recommendations]
    R --> F
>>>>>>> bdcb0f4 (Update student performance application)
```

## Dataset Description

The dataset in [dataset/student_performance.csv](dataset/student_performance.csv) includes:

<<<<<<< HEAD
### Dataset

The project uses a dataset containing **500 student records** and **6 columns**.

The six columns are:

```text
attendance
internal_marks
assignment_percentage
study_hours
previous_marks
performance
```

### Input Features

The machine learning model uses five input features:

| Feature | Description |
|---|---|
| Attendance | Student attendance percentage |
| Internal Marks | Internal examination marks |
| Assignment Percentage | Assignment completion percentage |
| Study Hours | Average study hours per day |
| Previous Marks | Previous academic marks |

### Target Variable

The target variable is:
=======
- attendance
- internal_marks
- assignment_percentage
- study_hours
- previous_marks
- performance

The target column is the categorical label for performance:

- Good
- Average
- Poor

## ML Workflow
>>>>>>> bdcb0f4 (Update student performance application)

1. Load the dataset.
2. Split the dataset into train and test sets.
3. Train the Random Forest classifier.
4. Save the model, feature list, and encoder.
5. Expose prediction and analytics endpoints through FastAPI.
6. Evaluate model comparison metrics for alternate classifiers.

<<<<<<< HEAD
Possible target values:
=======
## Features Implemented
>>>>>>> bdcb0f4 (Update student performance application)

- Student performance prediction
- Confidence score
- Risk-level detection
- Personalized recommendations
- Feature importance display from model metadata
- What-if comparison workflow
- Prediction history stored in SQLite
- Analytics summary for historical predictions
- Downloadable plain-text report
- Responsive dashboard UI

<<<<<<< HEAD
### Machine Learning Algorithm
=======
## Model Comparison
>>>>>>> bdcb0f4 (Update student performance application)

The backend compares several classifiers using real metrics from the dataset:

- Logistic Regression
- Decision Tree
- Random Forest
- K-Nearest Neighbors
- SVM

<<<<<<< HEAD
### Training Process

```text
Student Dataset
      ↓
Data Loading
      ↓
Data Preprocessing
      ↓
Feature Selection
      ↓
Train/Test Split
      ↓
Random Forest Classifier
      ↓
Model Evaluation
      ↓
Save Trained Model
```
=======
Metrics returned by the API include:

- Accuracy
- Precision
- Recall
- F1-score
>>>>>>> bdcb0f4 (Update student performance application)

The best model is selected using the highest F1 score, while the current Random Forest remains the production fallback used by the app.

## API Endpoints

### GET /
Returns a basic service status message.

### GET /health
Returns health and model status.

<<<<<<< HEAD
> Model performance can change if the dataset, preprocessing, train/test split, or model configuration is changed.

### Saved Model

The trained model is stored at:

```text
backend/model/student_model.pkl
```
=======
### POST /predict
Returns:
>>>>>>> bdcb0f4 (Update student performance application)

- prediction
- confidence
- risk_level
- reasons
- recommendations
- feature_importance

<<<<<<< HEAD
## 🧪 Prediction Example
=======
### GET /feature-importance
Returns feature names and importances from the trained model.
>>>>>>> bdcb0f4 (Update student performance application)

### GET /model-comparison
Returns comparison metrics for multiple classifiers.

### GET /prediction-history
Returns stored prediction history.

### GET /analytics
Returns aggregate prediction statistics.

### POST /what-if
Compares the current input with modified input and returns the change in prediction.

<<<<<<< HEAD
The confidence value depends on the input and trained model.

---

## ✨ Key Features

- AI-based student performance prediction
- Random Forest classification
- React frontend
- FastAPI REST API
- Prediction confidence
- Input validation
- Pytest API testing
- Docker containerization
- GitHub Actions CI
- Automated frontend build
- Automated Docker build
- Render backend deployment
- Render frontend deployment
- Public API documentation
- Health check endpoint

---

## 🔄 CI/CD Pipeline

This project uses **GitHub Actions** for Continuous Integration and **Render** for Continuous Deployment.

### CI/CD Flow

```text
Code Change
    ↓
Git Commit
    ↓
Git Push
    ↓
GitHub Repository
    ↓
GitHub Actions
    ↓
Install Python Dependencies
    ↓
Run Pytest
    ↓
Build Docker Image
    ↓
Install Frontend Dependencies
    ↓
Build React Frontend
    ↓
CI Success
    ↓
Render Auto Deployment
    ↓
Live Application
```

### Continuous Integration

GitHub Actions automatically performs:

- Checkout repository
- Setup Python
- Install backend dependencies
- Run Pytest
- Build Docker image
- Setup Node.js
- Install frontend dependencies
- Build React frontend

### Continuous Deployment

After successful changes are pushed to the `main` branch:

```text
GitHub
   ↓
GitHub Actions
   ↓
Tests + Builds
   ↓
Render
   ↓
Automatic Deployment
```

---

## ✅ CI Pipeline

The GitHub Actions workflow is located at:

```text
.github/workflows/ci-cd.yml
```

The workflow is triggered on:

```text
push → main
pull request → main
```

### Current CI Checks

```text
Backend Tests      ✅
Docker Build       ✅
Frontend Build     ✅
```

---

## 🐳 Docker

The FastAPI backend is containerized using Docker.

### Dockerfile

The project contains:

```text
Dockerfile
```

### Build Docker Image

```bash
docker build -t student-performance-api .
```

### Run Docker Container

```bash
docker run -d --name student-performance-container -p 8000:8000 student-performance-api
```

### Check Container

```bash
docker ps
```

### Local Backend URL

```text
http://127.0.0.1:8000
```
=======
## Frontend Structure
>>>>>>> bdcb0f4 (Update student performance application)

- [frontend/index.html](frontend/index.html)
- [frontend/src/main.jsx](frontend/src/main.jsx)
- [frontend/src/style.css](frontend/src/style.css)

The frontend provides:

- Student data entry form
- Prediction result cards
- Personalized recommendations
- Risk and analytics summary
- What-if comparison panel
- Prediction history list
- Feature importance bar visualization
- Report download button

<<<<<<< HEAD
### Test Cases

The project tests:

- Home endpoint
- Health endpoint
- Prediction endpoint

### Run Tests

From the project root:
=======
## Database

A lightweight SQLite database is used for storing prediction history.

Database file:
>>>>>>> bdcb0f4 (Update student performance application)

- [backend/student_performance.db](backend/student_performance.db)

The schema stores results such as:

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

<<<<<<< HEAD
Warnings may appear during testing, but the important result is that all tests pass successfully.

---

## 🔌 API Documentation

### Home Endpoint

```http
GET /
```

Example response:

```json
{
  "message": "Student Performance Prediction API is running"
}
```

---

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "model_loaded": true
}
```

---

### Prediction Endpoint

```http
POST /predict
```

Request:

```json
{
  "attendance": 85,
  "internal_marks": 78,
  "assignment_percentage": 90,
  "study_hours": 4,
  "previous_marks": 82
}
```

Response:

```json
{
  "prediction": "Good",
  "confidence": 66.0
}
```

---

## 🔐 Input Validation

The FastAPI backend validates the input values.

| Input | Valid Range |
|---|---|
| Attendance | 0–100 |
| Internal Marks | 0–100 |
| Assignment Percentage | 0–100 |
| Study Hours | 0–24 |
| Previous Marks | 0–100 |

Invalid values are rejected by the API.

---

## 🖥️ Frontend

The frontend is developed using:

- React
- JavaScript
- Vite
- CSS

### Frontend Features

- Student input form
- Input validation
- Prediction button
- Loading state
- Error handling
- Prediction result
- Confidence display
- Responsive UI

---

## 📸 Project Screenshots

### Live Student Performance Predictor

![Student Performance Predictor](screenshots/frontend.png)

### GitHub Actions CI Pipeline

![GitHub Actions CI Pipeline](screenshots/github-actions.png)

### Render Deployment

![Render Deployment](screenshots/render-deployment.png)

---

## 🛠️ Technology Stack

### Frontend

- React.js
- JavaScript
- Vite
- CSS

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

### Machine Learning

- Pandas
- Scikit-learn
- Random Forest
- Joblib

### Testing

- Pytest
- FastAPI TestClient

### DevOps / CI/CD

- Git
- GitHub
- GitHub Actions
- Docker
- Docker Compose
- Render

---

## 📂 Project Structure

```text
student-performance-cicd/
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   └── style.css
│   ├── index.html
│   ├── package.json
│   └── package-lock.json
│
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── model/
│   │   └── student_model.pkl
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_api.py
│   └── requirements.txt
│
├── dataset/
│   └── student_performance.csv
│
├── ml/
│   ├── train.py
│   └── preprocessing.py
│
├── screenshots/
│   ├── frontend.png
│   ├── github-actions.png
│   └── render-deployment.png
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── .gitignore
└── README.md
```

---

## ⚙️ Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/muralidharanv170807-spec/student-performance-cicd.git
```

```bash
cd student-performance-cicd
```

---

### 2. Create Python Virtual Environment

```powershell
python -m venv venv
```

Activate:
=======
## Docker

### Build

```bash
docker build -t student-performance-api .
```

### Run

```bash
docker run -d --name student-performance-container -p 8000:8000 student-performance-api
```

## CI/CD Pipeline

The GitHub Actions workflow runs:

- backend dependency installation
- backend test suite
- frontend dependency installation
- frontend production build
- Docker image build

Workflow file:

- [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml)

## Deployment

This project is ready for deployment on any compatible hosting platform. The backend exposes the prediction API through FastAPI and the frontend is served as a React app.

## How to Run Locally

### 1. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:
>>>>>>> bdcb0f4 (Update student performance application)

```powershell
.\venv\Scripts\Activate.ps1
```

<<<<<<< HEAD
---

### 3. Install Backend Dependencies

```powershell
pip install -r backend\requirements.txt
```

---

### 4. Start FastAPI Backend

```powershell
uvicorn backend.app:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

Health:

```text
http://127.0.0.1:8000/health
```

---

### 5. Start React Frontend

Open another terminal:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start:

```powershell
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 🧠 Train the Model

The training script is:

```text
ml/train.py
```

Run:

```powershell
python ml\train.py
```

The trained model will be saved to:

```text
backend/model/student_model.pkl
```

---

## 🌍 Deployment

### Backend Deployment

The FastAPI backend is deployed on Render:

```text
https://student-performance-cicd.onrender.com
```

### Frontend Deployment

The React frontend is deployed on Render:

```text
https://student-performance-cicd-1.onrender.com
```

### API Documentation

```text
https://student-performance-cicd.onrender.com/docs
```

### Health Check

```text
https://student-performance-cicd.onrender.com/health
```

---

## 🔁 Development Workflow

Whenever the project is updated:

```bash
git add .
```

```bash
git commit -m "Update project"
```

```bash
git push origin main
=======
### 2. Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Start the backend

```bash
uvicorn backend.app:app --reload
```

Visit:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

### 4. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Visit:

- http://localhost:5173

If you deploy the backend elsewhere, set the frontend environment variable:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000
>>>>>>> bdcb0f4 (Update student performance application)
```

## Environment Variables

- VITE_API_BASE_URL: frontend API endpoint override

## Testing

Run the backend tests:

```bash
python -m pytest -q
```

The project also verifies the frontend build with:

```bash
cd frontend
npm run build
```

## Future Enhancements

- Role-based access for staff versus students
- Authentication and user profiles
- More advanced charts and trend analysis
- Automated retraining pipeline
- Deployment-specific environment configuration

## Project Structure

```text
<<<<<<< HEAD
GitHub
   ↓
GitHub Actions
   ↓
Run Tests
   ↓
Build Docker
   ↓
Build Frontend
   ↓
Render Auto Deploy
   ↓
Updated Live Application
=======
student-performance-cicd-starter/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── model/
│   ├── tests/
│   └── student_performance.db
├── dataset/
│   └── student_performance.csv
├── frontend/
│   ├── index.html
│   ├── package.json
│   └── src/
├── ml/
│   └── train.py
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── README.md
└── .gitignore
>>>>>>> bdcb0f4 (Update student performance application)
```

## Notes

<<<<<<< HEAD
## 📚 Learning Outcomes

This project demonstrates practical experience with:

- Machine Learning classification
- Dataset handling
- Data preprocessing
- Model training
- Model evaluation
- Random Forest
- REST API development
- FastAPI
- React frontend development
- API integration
- Input validation
- Automated testing
- Pytest
- Docker
- Git
- GitHub
- GitHub Actions
- Continuous Integration
- Continuous Deployment
- Cloud deployment
- Render

---

## 🔮 Future Enhancements

Possible future improvements include:

- Student login and authentication
- Prediction history
- Database integration
- Student analytics dashboard
- Performance trend charts
- Feature importance visualization
- Multiple model comparison
- Automatic model retraining
- Model monitoring
- Faculty dashboard
- Student-specific reports

---

## 👨‍💻 Author

**Muralidharan V**

B.Tech Artificial Intelligence & Data Science

### GitHub

https://github.com/muralidharanv170807-spec

---

## ⭐ Project Summary

This project combines:

```text
Artificial Intelligence
        +
Machine Learning
        +
React
        +
FastAPI
        +
Docker
        +
GitHub Actions
        +
Continuous Integration
        +
Continuous Deployment
        +
Cloud Deployment
```

The complete workflow starts from **machine learning model development**, continues through **API and frontend development**, and ends with **automated testing, Docker containerization, CI/CD, and cloud deployment**.

---

## 📌 Repository

https://github.com/muralidharanv170807-spec/student-performance-cicd
=======
- The prediction logic is powered by the actual trained model.
- Risk thresholds and recommendation logic are defined in the backend as configurable values.
- All analytics and history come from the real app data and database records.
>>>>>>> bdcb0f4 (Update student performance application)
