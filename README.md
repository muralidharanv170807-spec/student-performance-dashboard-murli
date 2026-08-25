# 🎓 Student Performance Prediction Dashboard

A full-stack **Student Performance Prediction System** that uses Machine Learning to predict student academic performance and identify potential academic risks.

The application provides a React dashboard connected to a FastAPI backend and a trained Random Forest machine learning model.

## 🚀 Features

* 📊 Student performance prediction
* 🤖 Random Forest Machine Learning model
* 🎯 Performance classification:

  * Good
  * Average
  * Poor
* 📈 Prediction confidence
* ⚠️ Risk assessment:

  * Low
  * Medium
  * High
* 💡 Personalized recommendations
* 📋 Risk reasons
* 📊 Analytics dashboard
* 🔍 Feature importance
* 🔄 What-If analysis
* 🕒 Prediction history
* 📥 Downloadable student report
* 🗄️ SQLite database
* 🧪 Backend API testing
* 🐳 Docker support
* ⚙️ GitHub Actions CI/CD

## 🛠️ Technology Stack

### Frontend

* React
* Vite
* JavaScript
* CSS

### Backend

* Python
* FastAPI
* Pydantic
* SQLite

### Machine Learning

* scikit-learn
* Random Forest
* pandas
* joblib

### Development

* Pytest
* Docker
* GitHub Actions

## 📂 Project Structure

```text
student-performance-cicd-starter/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── model/
│   │   └── student_model.pkl
│   ├── tests/
│   │   └── test_api.py
│   └── student_performance.db
│
├── dataset/
│   └── student_performance.csv
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   └── src/
│       ├── main.jsx
│       └── style.css
│
├── ml/
│   ├── preprocessing.py
│   └── train.py
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── README.md
└── .gitignore
```

## 📊 Input Features

The application uses five student-related inputs:

| Feature               | Description                       |
| --------------------- | --------------------------------- |
| Attendance            | Student attendance percentage     |
| Internal Marks        | Internal examination marks        |
| Assignment Percentage | Assignment completion/performance |
| Study Hours           | Average study hours per day       |
| Previous Marks        | Previous academic marks           |

## 🤖 Machine Learning Model

The project uses a **Random Forest Classifier**.

The model predicts:

```text
Good
Average
Poor
```

The trained model is stored at:

```text
backend/model/student_model.pkl
```

The model uses:

```text
attendance
internal_marks
assignment_percentage
study_hours
previous_marks
```

## 🔄 How Prediction Works

```text
Student Input
     ↓
React Frontend
     ↓
POST /predict
     ↓
FastAPI Backend
     ↓
Random Forest Model
     ↓
Performance Prediction
     ↓
Risk Assessment
     ↓
Recommendations
     ↓
SQLite Prediction History
     ↓
Dashboard
```

## ⚠️ Risk Assessment

Risk assessment is separate from the machine-learning performance prediction.

The system evaluates factors such as:

* Attendance
* Internal marks
* Assignment performance
* Study hours
* Previous marks

Study hours of `0` are treated as a serious risk condition.

The risk levels are:

```text
LOW
MEDIUM
HIGH
```

Both **MEDIUM** and **HIGH** risk students are counted as at-risk students in the analytics.

## 📊 Analytics

The dashboard provides:

* Total Predictions
* Good Predictions
* Average Predictions
* Poor Predictions
* At-Risk Students
* Average Attendance
* Average Marks
* Average Study Hours

Analytics are calculated from the actual SQLite prediction history.

## 🔍 Feature Importance

The dashboard displays the feature importance obtained from the trained Random Forest model.

The features include:

* Study Hours
* Internal Marks
* Previous Marks
* Attendance
* Assignment Percentage

## 🔄 What-If Analysis

What-If Analysis allows you to compare:

```text
Current Student Inputs
          VS
Modified Student Inputs
```

The system shows how changing the student's inputs affects:

* Prediction
* Confidence
* Prediction outcome

What-If analysis does **not** create a new prediction-history record.

## 🕒 Prediction History

Successful predictions are stored in the SQLite database.

Each prediction can contain:

* Attendance
* Internal Marks
* Assignment Percentage
* Study Hours
* Previous Marks
* Prediction
* Confidence
* Risk Level
* Risk Reasons
* Recommendations
* Created Time

## 💻 Running the Project Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd student-performance-cicd-starter
```

### 2. Create the Python virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

### 5. Start the FastAPI backend

From the project root:

```bash
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend normally runs at:

```text
http://localhost:5173
```

Keep both the backend and frontend running while using the application.

## 🔗 API Endpoints

| Method | Endpoint              | Purpose                     |
| ------ | --------------------- | --------------------------- |
| GET    | `/`                   | API status                  |
| GET    | `/health`             | Backend/model health        |
| POST   | `/predict`            | Predict student performance |
| GET    | `/analytics`          | Dashboard analytics         |
| GET    | `/feature-importance` | Model feature importance    |
| GET    | `/model-comparison`   | Model comparison            |
| GET    | `/prediction-history` | Prediction history          |
| POST   | `/what-if`            | What-If analysis            |
| DELETE | `/prediction-history` | Clear development history   |

## 🧪 Testing

Run backend tests from the project root:

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

The project currently passes its backend test suite.

## 📦 Frontend Production Build

```bash
cd frontend
npm run build
```

The production files are generated in:

```text
frontend/dist
```

## 🐳 Docker

Build the image:

```bash
docker build -t student-performance-api .
```

Run it:

```bash
docker run -d --name student-performance-container -p 8000:8000 student-performance-api
```

Or:

```bash
docker-compose up --build
```

## ⚙️ CI/CD

The project includes GitHub Actions configuration in:

```text
.github/workflows/ci-cd.yml
```

The workflow checks:

* Backend dependencies
* Backend tests
* Frontend dependencies
* Frontend production build
* Docker image build

## 🌐 Live Demo

> Add your deployed application URL here after deploying the frontend and backend.

```text
Live Demo: COMING SOON
```

## 📌 Project Status

The application has been tested locally with:

* FastAPI backend
* React/Vite frontend
* Machine-learning prediction
* Analytics
* Feature importance
* Prediction history
* What-If analysis
* Risk assessment

## 👨‍💻 Author

**Student Performance Prediction Dashboard**

Built as a Machine Learning + Full-Stack application project.
