"""FastAPI Backend for Smart Salary Predictor System."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
import pandas as pd
import numpy as np
import joblib
import json
from datetime import datetime

from configs.config import (
    SALARY_MODEL_CONFIG,
    HISTORY_FILE,
    RAW_DATA_DIR,
    ARTIFACTS_DIR
)
from src.utils.helpers import (
    save_prediction_history,
    get_prediction_history,
    clear_prediction_history,
    validate_salary_input,
    setup_logging
)

# Setup logging
logger = setup_logging()

# Initialize FastAPI app
app = FastAPI(
    title="Smart Salary Predictor & Job Market Insights API",
    description="ML-powered salary prediction and income classification API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Pydantic Models ====================

class SalaryPredictionRequest(BaseModel):
    job_title: str = Field(..., description="Job title (e.g., Software Engineer)")
    experience_years: float = Field(..., ge=0, description="Years of experience")
    education_level: str = Field(..., description="Education level (e.g., Bachelor, Master)")
    skills_count: int = Field(..., ge=0, description="Number of skills")
    industry: str = Field(..., description="Industry (e.g., Technology, Finance)")
    company_size: str = Field(..., description="Company size (e.g., Startup, Large)")
    location: str = Field(..., description="Location (e.g., San Francisco, New York)")
    remote_work: str = Field(..., description="Remote work type (Fully Remote, Hybrid, On-site)")
    certifications: str = Field(..., description="Certifications (e.g., AWS Certified, None)")

class PredictionResponse(BaseModel):
    prediction: Any
    confidence: Optional[float] = None
    model_used: str
    top_features: Optional[List[Dict[str, float]]] = None
    timestamp: str

class ModelStatus(BaseModel):
    salary_model_loaded: bool
    salary_model_path: str

class PredictionHistory(BaseModel):
    history: List[Dict[str, Any]]
    total_count: int

class RetrainResponse(BaseModel):
    status: str
    message: str
    model_type: str
    results: Optional[Dict] = None

# ==================== Model Loading ====================

class ModelManager:
    """Manage ML models and preprocessors."""
    
    def __init__(self):
        self.salary_model = None
        self.salary_preprocessor = None
        self.load_models()
    
    def load_models(self):
        """Load all models and preprocessors."""
        try:
            if SALARY_MODEL_CONFIG["model_path"].exists():
                self.salary_model = joblib.load(SALARY_MODEL_CONFIG["model_path"])
                logger.info("Salary model loaded successfully")
            
            if SALARY_MODEL_CONFIG["preprocessor_path"].exists():
                self.salary_preprocessor = joblib.load(SALARY_MODEL_CONFIG["preprocessor_path"])
                logger.info("Salary preprocessor loaded successfully")
                
        except Exception as e:
            logger.error(f"Error loading models: {e}")
    
    def reload_models(self):
        """Reload all models."""
        self.load_models()

model_manager = ModelManager()

# ==================== API Endpoints ====================

@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Smart Salary Predictor & Job Market Insights API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/model-status", response_model=ModelStatus)
def get_model_status():
    """Get model loading status."""
    return ModelStatus(
        salary_model_loaded=model_manager.salary_model is not None,
        salary_model_path=str(SALARY_MODEL_CONFIG["model_path"])
    )

@app.post("/predict-salary", response_model=PredictionResponse)
def predict_salary(request: SalaryPredictionRequest):
    """Predict exact salary."""
    if model_manager.salary_model is None or model_manager.salary_preprocessor is None:
        raise HTTPException(status_code=503, detail="Salary model not loaded")
    
    try:
        # Prepare input data
        input_data = {
            "job_title": request.job_title,
            "experience_years": request.experience_years,
            "education_level": request.education_level,
            "skills_count": request.skills_count,
            "industry": request.industry,
            "company_size": request.company_size,
            "location": request.location,
            "remote_work": request.remote_work,
            "certifications": request.certifications
        }
        
        # Create DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Transform features
        features = model_manager.salary_preprocessor.transform(input_df)
        
        # Make prediction
        prediction = model_manager.salary_model.predict(features)[0]
        
        # Get confidence (for some models)
        confidence = None
        if hasattr(model_manager.salary_model, 'estimators_'):
            # For ensemble models, we can estimate variance
            predictions = [est.predict(features)[0] for est in model_manager.salary_model.estimators_]
            confidence = 1 - (np.std(predictions) / np.mean(predictions)) if np.mean(predictions) > 0 else 0
        
        # Get feature importance if available
        top_features = None
        if hasattr(model_manager.salary_model, 'feature_importances_'):
            importances = model_manager.salary_model.feature_importances_
            top_indices = np.argsort(importances)[-5:][::-1]
            try:
                feature_names = model_manager.salary_preprocessor.get_feature_names_out()
                top_features = [
                    {"feature": feature_names[i], "importance": float(importances[i])}
                    for i in top_indices
                ]
            except:
                pass
        
        # Format prediction
        predicted_salary = round(float(prediction), 2)
        
        # Save to history
        save_prediction_history(
            HISTORY_FILE,
            "salary",
            request.dict(),
            predicted_salary,
            confidence
        )
        
        return PredictionResponse(
            prediction=predicted_salary,
            confidence=round(confidence, 4) if confidence else None,
            model_used="salary_regressor",
            top_features=top_features,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/prediction-history", response_model=PredictionHistory)
def get_history(limit: int = 100):
    """Get prediction history."""
    history = get_prediction_history(HISTORY_FILE, limit)
    return PredictionHistory(
        history=history,
        total_count=len(history)
    )

@app.delete("/prediction-history")
def clear_history():
    """Clear prediction history."""
    clear_prediction_history(HISTORY_FILE)
    return {"message": "Prediction history cleared"}

@app.post("/retrain-model", response_model=RetrainResponse)
def retrain_model(background_tasks: BackgroundTasks):
    """Retrain the salary model."""
    def retrain_task():
        try:
            from src.pipelines.train_salary_model import train_salary_model
            train_salary_model()
            # Reload models after training
            model_manager.reload_models()
        except Exception as e:
            logger.error(f"Retraining error: {e}")
    
    background_tasks.add_task(retrain_task)
    
    return RetrainResponse(
        status="started",
        message="Retraining of salary model started in background",
        model_type="salary"
    )

@app.post("/upload-dataset")
def upload_dataset(file: UploadFile = File(...)):
    """Upload a new salary dataset for training."""
    try:
        filepath = RAW_DATA_DIR / "salary_data.csv"
        
        with open(filepath, "wb") as f:
            f.write(file.file.read())
        
        return {
            "message": "Salary dataset uploaded successfully",
            "filepath": str(filepath),
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download-predictions")
def download_predictions():
    """Download prediction history as CSV."""
    try:
        history = get_prediction_history(HISTORY_FILE)
        
        if not history:
            raise HTTPException(status_code=404, detail="No predictions found")
        
        # Convert to DataFrame
        df = pd.json_normalize(history)
        
        # Save to CSV
        output_path = ARTIFACTS_DIR / "predictions_export.csv"
        df.to_csv(output_path, index=False)
        
        return {
            "message": "Predictions exported successfully",
            "filepath": str(output_path),
            "record_count": len(df)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feature-importance")
def get_feature_importance_endpoint():
    """Get feature importance for the salary model."""
    model = model_manager.salary_model
    preprocessor = model_manager.salary_preprocessor
    
    if model is None:
        raise HTTPException(status_code=503, detail="Salary model not loaded")
    
    if not hasattr(model, 'feature_importances_'):
        raise HTTPException(status_code=400, detail="Salary model doesn't support feature importance")
    
    importances = model.feature_importances_
    
    # Get feature names
    try:
        feature_names = preprocessor.get_feature_names_out()
    except:
        feature_names = [f"feature_{i}" for i in range(len(importances))]
    
    importance_dict = dict(zip(feature_names, importances))
    sorted_importance = dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
    
    return {
        "model_type": "salary",
        "feature_importance": sorted_importance
    }

# Run with: uvicorn backend.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
