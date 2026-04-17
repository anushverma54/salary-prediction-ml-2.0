"""Data loading and preprocessing utilities."""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, List, Optional
from sklearn.model_selection import train_test_split

class DataLoader:
    """Handle data loading and basic preprocessing."""
    
    def __init__(self, logger=None):
        self.logger = logger
    
    def load_income_data(self, filepath: Path) -> pd.DataFrame:
        """Load the Adult Income dataset."""
        if self.logger:
            self.logger.info(f"Loading income data from {filepath}")
        
        # Column names for Adult dataset
        columns = [
            "age", "workclass", "fnlwgt", "education", "education-num",
            "marital-status", "occupation", "relationship", "race", "gender",
            "capital-gain", "capital-loss", "hours-per-week", "native-country", "income"
        ]
        
        df = pd.read_csv(filepath, names=columns, na_values=" ?", skipinitialspace=True)
        
        # Drop fnlwgt as it's not useful for prediction
        df = df.drop("fnlwgt", axis=1)
        df = df.drop("education-num", axis=1)
        
        if self.logger:
            self.logger.info(f"Loaded {len(df)} rows")
        
        return df
    
    def load_salary_data(self, filepath: Path) -> pd.DataFrame:
        """Load the Job Salary Prediction dataset."""
        if self.logger:
            self.logger.info(f"Loading salary data from {filepath}")
        
        df = pd.read_csv(filepath)
        
        if self.logger:
            self.logger.info(f"Loaded {len(df)} rows")
        
        return df
    
    def handle_missing_values(self, df: pd.DataFrame, strategy: str = "drop") -> pd.DataFrame:
        """Handle missing values in the dataframe."""
        if self.logger:
            missing_before = df.isnull().sum().sum()
            self.logger.info(f"Missing values before: {missing_before}")
        
        if strategy == "drop":
            df = df.dropna()
        elif strategy == "fill_mode":
            for col in df.columns:
                if df[col].dtype == "object":
                    df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown")
                else:
                    df[col] = df[col].fillna(df[col].median())
        
        if self.logger:
            missing_after = df.isnull().sum().sum()
            self.logger.info(f"Missing values after: {missing_after}")
        
        return df
    
    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows."""
        before = len(df)
        df = df.drop_duplicates()
        after = len(df)
        
        if self.logger:
            self.logger.info(f"Removed {before - after} duplicate rows")
        
        return df
    
    def preprocess_income_target(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess income target variable."""
        # Convert income to binary
        df["income"] = df["income"].apply(
            lambda x: 1 if ">50K" in str(x) else 0
        )
        return df
    
    def split_data(
        self,
        df: pd.DataFrame,
        target_col: str,
        test_size: float = 0.2,
        random_state: int = 42
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Split data into train and test sets."""
        X = df.drop(target_col, axis=1)
        y = df[target_col]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y if y.dtype == "object" or len(y.unique()) < 10 else None
        )
        
        if self.logger:
            self.logger.info(f"Train set: {len(X_train)}, Test set: {len(X_test)}")
        
        return X_train, X_test, y_train, y_test

    def get_data_summary(self, df: pd.DataFrame) -> Dict:
        """Get summary statistics of the dataset."""
        summary = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns": list(df.columns),
            "dtypes": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "numeric_summary": df.describe().to_dict() if df.select_dtypes(include=[np.number]).shape[1] > 0 else {}
        }
        return summary
