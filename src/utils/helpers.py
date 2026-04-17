"""Helper utility functions."""
import json
import logging
from pathlib import Path
from typing import Any, Dict, List
import joblib
import pandas as pd
from datetime import datetime

# Setup logging
def setup_logging(log_file: Path = None) -> logging.Logger:
    """Setup logging configuration."""
    logger = logging.getLogger("salary_predictor")
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Save/Load models
def save_model(model: Any, filepath: Path) -> None:
    """Save a trained model to disk."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, filepath)

def load_model(filepath: Path) -> Any:
    """Load a trained model from disk."""
    if not filepath.exists():
        raise FileNotFoundError(f"Model file not found: {filepath}")
    return joblib.load(filepath)

# Prediction history
def save_prediction_history(
    history_file: Path,
    prediction_type: str,
    input_data: Dict,
    prediction: Any,
    confidence: float = None
) -> None:
    """Save prediction to history file."""
    history_file.parent.mkdir(parents=True, exist_ok=True)
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": prediction_type,
        "input": input_data,
        "prediction": prediction,
        "confidence": confidence
    }
    
    history = []
    if history_file.exists():
        with open(history_file, 'r') as f:
            history = json.load(f)
    
    history.append(entry)
    
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2, default=str)

def get_prediction_history(history_file: Path, limit: int = 100) -> List[Dict]:
    """Get prediction history from file."""
    if not history_file.exists():
        return []
    
    with open(history_file, 'r') as f:
        history = json.load(f)
    
    return history[-limit:]

def clear_prediction_history(history_file: Path) -> None:
    """Clear prediction history."""
    if history_file.exists():
        with open(history_file, 'w') as f:
            json.dump([], f)

# Data validation
def validate_income_input(data: Dict) -> tuple[bool, str]:
    """Validate income prediction input data."""
    required_fields = [
        "age", "education", "occupation", "workclass",
        "gender", "marital_status", "hours_per_week", "native_country"
    ]
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    if not isinstance(data["age"], (int, float)) or data["age"] < 0:
        return False, "Age must be a positive number"
    
    if not isinstance(data["hours_per_week"], (int, float)) or data["hours_per_week"] < 0:
        return False, "Hours per week must be a positive number"
    
    return True, "Valid"

def validate_salary_input(data: Dict) -> tuple[bool, str]:
    """Validate salary prediction input data."""
    required_fields = [
        "job_title", "experience_years", "education_level", "skills_count",
        "industry", "company_size", "location", "remote_work", "certifications"
    ]
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    if not isinstance(data["experience_years"], (int, float)) or data["experience_years"] < 0:
        return False, "Experience years must be a positive number"
    
    if not isinstance(data["skills_count"], (int, float)) or data["skills_count"] < 0:
        return False, "Skills count must be a positive number"
    
    return True, "Valid"

# Export functions
def export_predictions_to_csv(predictions: List[Dict], filepath: Path) -> None:
    """Export predictions to CSV file."""
    df = pd.DataFrame(predictions)
    df.to_csv(filepath, index=False)
