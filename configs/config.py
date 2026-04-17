"""Configuration settings for the Salary Prediction ML System."""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"

# Ensure directories exist
for dir_path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, ARTIFACTS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Regression Model Config
SALARY_MODEL_CONFIG = {
    "model_path": ARTIFACTS_DIR / "salary_model.pkl",
    "preprocessor_path": ARTIFACTS_DIR / "salary_preprocessor.pkl",
    "test_size": 0.2,
    "random_state": 42,
    "models_to_train": ["linear_regression", "decision_tree", "random_forest"],
    "features": [
        "job_title",
        "experience_years",
        "education_level",
        "skills_count",
        "industry",
        "company_size",
        "location",
        "remote_work",
        "certifications"
    ],
    "target": "salary",
    "categorical_features": [
        "job_title",
        "education_level",
        "industry",
        "company_size",
        "location",
        "remote_work",
        "certifications"
    ],
    "numerical_features": [
        "experience_years",
        "skills_count"
    ]
}

# API Config
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "reload": True
}

# Dashboard Config
DASHBOARD_CONFIG = {
    "title": "Smart Salary Predictor & Job Market Insights",
    "page_icon": "💼",
    "layout": "wide"
}

# Prediction History
HISTORY_FILE = ARTIFACTS_DIR / "prediction_history.json"
