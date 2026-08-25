# 🎓 Student Performance Prediction Dashboard

A full-stack **Student Performance Prediction System** that uses Machine Learning to predict student academic performance and identify potential academic risks.

The application consists of a **React + Vite frontend**, a **FastAPI backend**, a trained **Random Forest machine-learning model**, and a **SQLite database** for prediction history.

---

## 🌐 Live Application

### 🚀 Frontend

**Student Performance Dashboard**

https://student-performance-dashboard-murli.onrender.com

### ⚙️ Backend API

**Student Performance Prediction API**

https://student-performance-api-murli.onrender.com

### 📖 API Documentation

https://student-performance-api-murli.onrender.com/docs

> The backend API is deployed separately from the frontend.

---

## 🚀 Features

- 📊 Student performance prediction
- 🤖 Random Forest Machine Learning model
- 🎯 Performance classification:
  - Good
  - Average
  - Poor
- 📈 Prediction confidence
- ⚠️ Risk assessment:
  - Low
  - Medium
  - High
- 💡 Personalized recommendations
- 📋 Risk reasons
- 📊 Analytics dashboard
- 🔍 Feature importance
- 🔄 What-If analysis
- 🕒 Prediction history
- 📥 Downloadable student report
- 🗄️ SQLite database
- 🧪 Backend API testing
- 🐳 Docker support
- ⚙️ GitHub Actions CI/CD

---

## 🛠️ Technology Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- FastAPI
- Pydantic
- SQLite

### Machine Learning

- scikit-learn
- Random Forest
- pandas
- joblib

### Development & Deployment

- Pytest
- Docker
- GitHub Actions
- Render

---

## 📂 Project Structure

```text
student-performance-dashboard-murli/
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
