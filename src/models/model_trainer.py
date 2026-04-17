"""Model training and evaluation module."""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
    mean_absolute_error, mean_squared_error, r2_score
)
import joblib
from pathlib import Path
import json

class ModelTrainer:
    """Train and evaluate machine learning models."""
    
    def __init__(self, logger=None):
        self.logger = logger
        self.trained_models = {}
        self.best_model = None
        self.best_model_name = None
        self.metrics = {}
    
    def train_classification_models(
        self,
        X_train: np.ndarray,
        X_test: np.ndarray,
        y_train: np.ndarray,
        y_test: np.ndarray,
        models: List[str] = ["logistic_regression", "decision_tree", "random_forest"]
    ) -> Dict[str, Any]:
        """Train multiple classification models and return results."""
        if self.logger:
            self.logger.info("Training classification models...")
        
        available_models = {
            "logistic_regression": LogisticRegression(max_iter=1000, random_state=42),
            "decision_tree": DecisionTreeClassifier(random_state=42, max_depth=10),
            "random_forest": RandomForestClassifier(n_estimators=100, random_state=42, max_depth=15)
        }
        
        results = {}
        best_f1 = 0
        
        for model_name in models:
            if model_name not in available_models:
                continue
            
            if self.logger:
                self.logger.info(f"Training {model_name}...")
            
            model = available_models[model_name]
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred = model.predict(X_test)
            
            # Metrics
            metrics = {
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred, average='weighted', zero_division=0),
                "recall": recall_score(y_test, y_pred, average='weighted', zero_division=0),
                "f1_score": f1_score(y_test, y_pred, average='weighted', zero_division=0),
                "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()
            }
            
            results[model_name] = {
                "model": model,
                "metrics": metrics
            }
            
            # Track best model
            if metrics["f1_score"] > best_f1:
                best_f1 = metrics["f1_score"]
                self.best_model = model
                self.best_model_name = model_name
            
            if self.logger:
                self.logger.info(f"{model_name} - F1: {metrics['f1_score']:.4f}")
        
        self.trained_models = results
        return results
    
    def train_regression_models(
        self,
        X_train: np.ndarray,
        X_test: np.ndarray,
        y_train: np.ndarray,
        y_test: np.ndarray,
        models: List[str] = ["linear_regression", "decision_tree", "random_forest"]
    ) -> Dict[str, Any]:
        """Train multiple regression models and return results."""
        if self.logger:
            self.logger.info("Training regression models...")
        
        available_models = {
            "linear_regression": LinearRegression(),
            "decision_tree": DecisionTreeRegressor(random_state=42, max_depth=10),
            "random_forest": RandomForestRegressor(n_estimators=100, random_state=42, max_depth=15)
        }
        
        results = {}
        best_r2 = -np.inf
        
        for model_name in models:
            if model_name not in available_models:
                continue
            
            if self.logger:
                self.logger.info(f"Training {model_name}...")
            
            model = available_models[model_name]
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred = model.predict(X_test)
            
            # Metrics
            metrics = {
                "mae": mean_absolute_error(y_test, y_pred),
                "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
                "r2_score": r2_score(y_test, y_pred)
            }
            
            results[model_name] = {
                "model": model,
                "metrics": metrics
            }
            
            # Track best model (using R2 score)
            if metrics["r2_score"] > best_r2:
                best_r2 = metrics["r2_score"]
                self.best_model = model
                self.best_model_name = model_name
            
            if self.logger:
                self.logger.info(f"{model_name} - R2: {metrics['r2_score']:.4f}, RMSE: {metrics['rmse']:.2f}")
        
        self.trained_models = results
        return results
    
    def save_best_model(self, filepath: Path) -> None:
        """Save the best model to disk."""
        if self.best_model is None:
            raise ValueError("No model has been trained yet.")
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.best_model, filepath)
        
        # Save metadata
        metadata = {
            "model_name": self.best_model_name,
            "model_type": "classification" if hasattr(self.best_model, "classes_") else "regression"
        }
        
        metadata_path = filepath.parent / f"{filepath.stem}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        if self.logger:
            self.logger.info(f"Best model ({self.best_model_name}) saved to {filepath}")
    
    def load_model(self, filepath: Path) -> Any:
        """Load a trained model from disk."""
        model = joblib.load(filepath)
        if self.logger:
            self.logger.info(f"Model loaded from {filepath}")
        return model
    
    def get_feature_importance(self, feature_names: List[str] = None) -> Dict[str, float]:
        """Get feature importance from the best model."""
        if self.best_model is None:
            raise ValueError("No model has been trained yet.")
        
        if hasattr(self.best_model, 'feature_importances_'):
            importances = self.best_model.feature_importances_
        elif hasattr(self.best_model, 'coef_'):
            importances = np.abs(self.best_model.coef_)
            if importances.ndim > 1:
                importances = importances.mean(axis=0)
        else:
            return {}
        
        if feature_names is not None:
            return dict(zip(feature_names, importances))
        return {f"feature_{i}": imp for i, imp in enumerate(importances)}
    
    def get_comparison_table(self) -> pd.DataFrame:
        """Get a comparison table of all trained models."""
        if not self.trained_models:
            return pd.DataFrame()
        
        data = []
        for model_name, result in self.trained_models.items():
            row = {"Model": model_name}
            row.update(result["metrics"])
            data.append(row)
        
        return pd.DataFrame(data)
