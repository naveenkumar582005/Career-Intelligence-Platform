# Career Intelligence Platform

An AI-powered, multi-module web platform for placement prediction, PDF resume parsing, NLP job role recommendation, skill gap analysis, and personalized career roadmap generation.

---

## Key Features

- **Machine Learning Placement Prediction**: Predicts placement outcomes ("Placed" vs. "Not Placed") and confidence probability % using an 8-feature model.
- **Hybrid Resume Parsing**: Extracts structured text, contact info, known tech skills, and out-of-vocabulary skills from PDF resumes using `pdfplumber` and regex heuristics.
- **Multi-Dimensional Readiness Metrics**: Computes **Resume Score**, **Technical Strength**, **Industry Readiness**, and **Career Readiness**.
- **NLP Job Recommendation**: Ranks top matching job roles using **TF-IDF Vectorization** and **Cosine Similarity** against market job datasets.
- **Skill Gap & Certification Engine**: Identifies missing skill tokens for target job roles and recommends industry certifications.
- **Personalized Career Roadmap**: Maps missing skills to actionable learning tasks with timeline estimates.
- **Explainable AI Analytics**: Generates server-side SHAP-style visual analytics and feature impact charts.
- **Report Download**: Exports complete candidate assessment summaries as downloadable text files.

---

## Technology Stack

- **Backend REST API (Port 5000)**: Python 3, Flask, Flask-CORS, Werkzeug
- **Machine Learning & NLP**: Scikit-Learn (StandardScaler, LabelEncoder, Classifier, TfidfVectorizer), Joblib, NumPy, Pandas, `pdfplumber`
- **Visualization**: Matplotlib (`Agg` server-side backend)
- **Frontend App (Port 3000)**: HTML5, Custom CSS3 (Dark mode, design tokens), Vanilla JavaScript ES6+ (Async Fetch API), Bootstrap 5.3.3, Bootstrap Icons

---

## Project Structure

```text
Career-Intelligence-Platform/
├── backend/                  # Backend REST API Server (Port 5000)
│   ├── app.py                # Flask REST API endpoints & CORS handler
│   ├── config.py             # Backend paths & system limits
│   ├── requirements.txt      # Backend Python dependencies
│   ├── dataset/              # Job market CSV dataset (jobs.csv)
│   ├── model/                # Pre-trained ML pickle models (.pkl)
│   ├── uploads/              # Uploaded PDF resume folder
│   ├── static/images/        # Generated dynamic Matplotlib charts
│   └── utils/                # ML predictor, resume parser, scoring, skill matcher, roadmap & chart engines
│
└── frontend/                 # Frontend Web Application (Port 3000)
    ├── server.py             # Frontend Web Application Server
    ├── templates/            # HTML5 views (index.html, upload.html, dashboard.html, etc.)
    └── static/               # CSS stylesheet & client JavaScript (communicates with http://localhost:5000)
```

---

## Installation & Running Guide

### 1. Install Backend Dependencies

```bash
pip install -r backend/requirements.txt
```

### 2. Run the Platform (Decoupled Stack)

#### Terminal 1 — Start Backend REST API (Port 5000):
```bash
cd backend
python app.py
```
*Backend API will run on `http://localhost:5000`*

#### Terminal 2 — Start Frontend Web App (Port 3000):
```bash
cd frontend
python server.py
```
*Frontend Application will run on `http://localhost:3000`*

---

## Access Application

Open your browser and navigate to:
```
http://localhost:3000
```
