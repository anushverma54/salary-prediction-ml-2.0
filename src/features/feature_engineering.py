"""Feature engineering and preprocessing pipelines."""
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
import joblib
from pathlib import Path
from typing import List, Tuple

class FeatureEngineer:
    """Handle feature engineering and preprocessing."""
    
    def __init__(self, logger=None):
        self.logger = logger
        self.preprocessor = None
    
    def create_preprocessor(
        self,
        categorical_features: List[str],
        numerical_features: List[str]
    ) -> ColumnTransformer:
        """Create preprocessing pipeline for features."""
        if self.logger:
            self.logger.info("Creating feature preprocessor")
        
        # Categorical pipeline
        categorical_pipeline = Pipeline([
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])
        
        # Numerical pipeline
        numerical_pipeline = Pipeline([
            ('scaler', StandardScaler())
        ])
        
        # Combine pipelines
        preprocessor = ColumnTransformer([
            ('cat', categorical_pipeline, categorical_features),
            ('num', numerical_pipeline, numerical_features)
        ], remainder='drop')
        
        self.preprocessor = preprocessor
        return preprocessor
    
    def fit_transform(
        self,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Fit and transform training data, transform test data."""
        X_train_transformed = self.preprocessor.fit_transform(X_train)
        
        if X_test is not None:
            X_test_transformed = self.preprocessor.transform(X_test)
            return X_train_transformed, X_test_transformed
        
        return X_train_transformed, None
    
    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """Transform data using fitted preprocessor."""
        if self.preprocessor is None:
            raise ValueError("Preprocessor not fitted. Call fit_transform first.")
        return self.preprocessor.transform(X)
    
    def save_preprocessor(self, filepath: Path) -> None:
        """Save the fitted preprocessor."""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.preprocessor, filepath)
        if self.logger:
            self.logger.info(f"Preprocessor saved to {filepath}")
    
    def load_preprocessor(self, filepath: Path) -> None:
        """Load a fitted preprocessor."""
        self.preprocessor = joblib.load(filepath)
        if self.logger:
            self.logger.info(f"Preprocessor loaded from {filepath}")
    
    def get_feature_names(self, categorical_features: List[str], numerical_features: List[str]) -> List[str]:
        """Get feature names after transformation."""
        if self.preprocessor is None:
            raise ValueError("Preprocessor not fitted.")
        
        feature_names = []
        
        # Get categorical feature names from one-hot encoder
        cat_encoder = self.preprocessor.named_transformers_['cat'].named_steps['onehot']
        cat_features = cat_encoder.get_feature_names_out(categorical_features)
        feature_names.extend(cat_features)
        
        # Add numerical feature names
        feature_names.extend(numerical_features)
        
        return list(feature_names)


class IncomeFeatureEngineer(FeatureEngineer):
    """Feature engineering specific to Income Classification."""
    
    def __init__(self, logger=None):
        super().__init__(logger)
        self.categorical_features = [
            "workclass", "education", "marital-status", "occupation",
            "relationship", "race", "gender", "native-country"
        ]
        self.numerical_features = [
            "age", "capital-gain", "capital-loss", "hours-per-week"
        ]
    
    def create_income_preprocessor(self) -> ColumnTransformer:
        """Create preprocessor for income classification."""
        return self.create_preprocessor(self.categorical_features, self.numerical_features)
    
    def get_income_feature_names(self) -> List[str]:
        """Get feature names for income model."""
        return self.get_feature_names(self.categorical_features, self.numerical_features)


class SalaryFeatureEngineer(FeatureEngineer):
    """Feature engineering specific to Salary Regression."""
    
    def __init__(self, logger=None):
        super().__init__(logger)
        self.categorical_features = [
            "job_title", "education_level", "industry", "company_size",
            "location", "remote_work", "certifications"
        ]
        self.numerical_features = [
            "experience_years", "skills_count"
        ]
    
    def create_salary_preprocessor(self) -> ColumnTransformer:
        """Create preprocessor for salary regression."""
        return self.create_preprocessor(self.categorical_features, self.numerical_features)
    
    def get_salary_feature_names(self) -> List[str]:
        """Get feature names for salary model."""
        return self.get_feature_names(self.categorical_features, self.numerical_features)
