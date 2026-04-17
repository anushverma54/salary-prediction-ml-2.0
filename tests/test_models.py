"""Unit tests for ML models."""
import unittest
import sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent))

from src.models.model_trainer import ModelTrainer


class TestModelTrainer(unittest.TestCase):
    """Test cases for ModelTrainer."""
    
    def setUp(self):
        """Set up test data."""
        self.X_train = np.random.randn(100, 10)
        self.X_test = np.random.randn(20, 10)
        self.y_train = np.random.randint(0, 2, 100)
        self.y_test = np.random.randint(0, 2, 20)
    
    def test_train_classification_models(self):
        """Test classification model training."""
        trainer = ModelTrainer()
        results = trainer.train_classification_models(
            self.X_train, self.X_test, self.y_train, self.y_test,
            models=["logistic_regression"]
        )
        
        self.assertIn("logistic_regression", results)
        self.assertIn("metrics", results["logistic_regression"])
        self.assertIn("accuracy", results["logistic_regression"]["metrics"])
    
    def test_train_regression_models(self):
        """Test regression model training."""
        y_train_reg = np.random.randn(100) * 10000 + 50000
        y_test_reg = np.random.randn(20) * 10000 + 50000
        
        trainer = ModelTrainer()
        results = trainer.train_regression_models(
            self.X_train, self.X_test, y_train_reg, y_test_reg,
            models=["linear_regression"]
        )
        
        self.assertIn("linear_regression", results)
        self.assertIn("metrics", results["linear_regression"])
        self.assertIn("r2_score", results["linear_regression"]["metrics"])
    
    def test_comparison_table(self):
        """Test model comparison table generation."""
        trainer = ModelTrainer()
        trainer.train_classification_models(
            self.X_train, self.X_test, self.y_train, self.y_test,
            models=["logistic_regression"]
        )
        
        comparison = trainer.get_comparison_table()
        self.assertIsNotNone(comparison)
        self.assertIn("Model", comparison.columns)


class TestDataLoader(unittest.TestCase):
    """Test cases for DataLoader."""
    
    def test_preprocess_income_target(self):
        """Test income target preprocessing."""
        from src.data.data_loader import DataLoader
        
        df = pd.DataFrame({
            'income': ['<=50K', '>50K', '<=50K', '>50K']
        })
        
        loader = DataLoader()
        processed = loader.preprocess_income_target(df)
        
        self.assertEqual(processed['income'].iloc[0], 0)
        self.assertEqual(processed['income'].iloc[1], 1)


if __name__ == '__main__':
    unittest.main()
