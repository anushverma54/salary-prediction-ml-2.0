# 💰 Smart Salary Predictor System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green)](https://fastapi.tiangolo.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3%2B-orange)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)](https://streamlit.io/)

An AI-powered salary prediction system with a unified Streamlit dashboard and FastAPI backend. Get instant salary estimates, explore job market insights, and understand what drives your earning potential.

![Project Banner](https://img.shields.io/badge/ML-Salary%20Prediction-success?style=for-the-badge)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [ML Models](#ml-models)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🔮 AI-Powered Salary Prediction

- **Popup-Style Results**: Large, prominent salary display at the top - no scrolling required!
- **Exact Salary Prediction**: Get precise salary estimates in USD
- **Machine Learning Models**: Linear Regression, Decision Tree, Random Forest
- **Auto Model Selection**: Best model chosen by R² score
- **Confidence Indicators**: See prediction reliability with visual progress bars
- **Salary Breakdown**: View monthly, bi-weekly, and weekly estimates
- **Feature Importance**: Understand what factors drive your salary

### 📊 Unified Streamlit Dashboard

All functionality in one place - no separate frontend needed!

- **🔮 Predict Salary**: Interactive form with popup-style results
- **📊 Analytics**: Comprehensive job market insights
  - Industry salary comparisons
  - Experience vs salary trends
  - Job title analysis
  - Remote work impact
- **🔍 Feature Importance**: Top factors affecting salaries
- **📈 Model Performance**: Training metrics and model evaluation
- **⚙️ Admin Panel**:
  - Retrain models with one click
  - Upload custom datasets
  - View prediction history
  - Download predictions as CSV

### 📈 Visualizations

- Interactive Plotly charts
- Industry-based salary comparisons
- Experience vs salary correlation
- Location-based compensation analysis
- Remote work impact on salaries
- Certification value analysis

### 🔧 Production Features

- **FastAPI Backend** with async support
- **25,000 Sample Dataset** for robust predictions
- CORS enabled for cross-origin requests
- Input validation with Pydantic models
- Automatic model retraining endpoint
- Dataset upload functionality
- Prediction history tracking
- Export predictions to CSV

## 🛠️ Tech Stack

### Machine Learning
- Python 3.8+
- scikit-learn (Regression Models)
- pandas (Data manipulation)
- numpy (Numerical computing)
- joblib (Model serialization)

### Backend
- FastAPI (Modern Python web framework)
- Uvicorn (ASGI server)
- Pydantic (Data validation)

### Dashboard
- Streamlit (All-in-one interface)
- Plotly (Interactive charts)
- Seaborn & Matplotlib (Static plots)

## 📁 Project Structure

```
salary-prediction-ml/
├── configs/
│   └── config.py                 # Configuration settings
├── data/
│   ├── raw/                      # Raw datasets (25,000 samples)
│   └── processed/                # Processed datasets
├── notebooks/                    # Jupyter notebooks for EDA
├── src/
│   ├── data/
│   │   └── data_loader.py        # Data loading utilities
│   ├── features/
│   │   └── feature_engineering.py # Feature preprocessing
│   ├── models/
│   │   └── model_trainer.py      # Model training & evaluation
│   ├── pipelines/
│   │   └── train_salary_model.py # Salary model training pipeline
│   ├── visualization/
│   │   └── visualizer.py         # Visualization utilities
│   └── utils/
│       └── helpers.py            # Helper functions
├── backend/
│   └── main.py                   # FastAPI application
├── dashboard/
│   └── app.py                    # Unified Streamlit dashboard
├── artifacts/                    # Saved models & preprocessors
├── tests/                        # Unit tests
├── requirements.txt              # Python dependencies
├── train_all.py                  # Training script
├── start_all.py                  # Startup script
├── README.md                     # This file
└── .gitignore                    # Git ignore rules
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/anushverma54/salary-prediction-ml-2.0.git
cd salary-prediction-ml-2.0
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Train the Model

```bash
python train_all.py
```

This creates a synthetic dataset with **25,000 samples** and trains the salary prediction model.

## 🎯 Usage

### Quick Start (Recommended)

Start both backend and dashboard with one command:

```bash
python start_all.py
```

This will start:
- **Dashboard**: http://localhost:8501 (Predictions + Analytics)
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Manual Start

If you prefer to start services separately:

**1. Start Backend:**
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**2. Start Dashboard:**
```bash
streamlit run dashboard/app.py
```

## 📡 API Documentation

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root - API info |
| `/health` | GET | Health check |
| `/model-status` | GET | Get model loading status |
| `/predict-salary` | POST | Salary prediction |
| `/prediction-history` | GET | Get prediction history |
| `/prediction-history` | DELETE | Clear prediction history |
| `/retrain-model` | POST | Retrain the salary model |
| `/upload-dataset` | POST | Upload new dataset |
| `/download-predictions` | GET | Download predictions as CSV |
| `/feature-importance` | GET | Get feature importance |

### Example API Request

#### Salary Prediction
```bash
curl -X POST "http://localhost:8000/predict-salary" \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Software Engineer",
    "experience_years": 5,
    "education_level": "Bachelor",
    "skills_count": 8,
    "industry": "Technology",
    "company_size": "Medium (201-1000)",
    "location": "San Francisco",
    "remote_work": "Hybrid",
    "certifications": "AWS Certified"
  }'
```

**Response:**
```json
{
  "prediction": 145000,
  "confidence": 0.89,
  "top_features": [
    {"feature": "job_title_Software Engineer", "importance": 0.25},
    {"feature": "location_San Francisco", "importance": 0.20},
    {"feature": "experience_years", "importance": 0.18}
  ]
}
```

## 🤖 ML Models

### Salary Regression Model

**Dataset**: Synthetic Salary Dataset
- **Size**: 25,000 samples
- **Features**: 9 input features
- **Target**: salary (numeric, USD)

**Input Features**:
| Feature | Type | Description |
|---------|------|-------------|
| job_title | Categorical | Job role (16 categories) |
| experience_years | Numeric | Years of experience (0-30) |
| education_level | Categorical | Highest education (6 levels) |
| skills_count | Numeric | Number of skills (1-25) |
| industry | Categorical | Industry sector (10 categories) |
| company_size | Categorical | Company size (4 categories) |
| location | Categorical | Work location (12 cities) |
| remote_work | Categorical | Remote work type (3 options) |
| certifications | Categorical | Certifications held (9 options) |

**Algorithms**:
- Linear Regression (best performing)
- Decision Tree Regressor
- Random Forest Regressor

**Evaluation Metrics**:
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² Score

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Streamlit](https://streamlit.io/) for the dashboard framework
- [scikit-learn](https://scikit-learn.org/) for the ML algorithms
- [Plotly](https://plotly.com/) for interactive visualizations

## 📧 Contact

Anush Verma - [GitHub](https://github.com/anushverma54)

Project Link: [https://github.com/anushverma54/salary-prediction-ml-2.0](https://github.com/anushverma54/salary-prediction-ml-2.0)

---

⭐ Star this repository if you find it helpful!
