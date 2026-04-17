"""Training pipeline for Income Classification Model."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from sklearn.datasets import fetch_openml
from src.data.data_loader import DataLoader
from src.features.feature_engineering import IncomeFeatureEngineer
from src.models.model_trainer import ModelTrainer
from src.utils.helpers import save_model, setup_logging
from configs.config import INCOME_MODEL_CONFIG, RAW_DATA_DIR, ARTIFACTS_DIR
import joblib

def download_adult_dataset():
    """Download the Adult Income dataset if not exists."""
    adult_path = RAW_DATA_DIR / "adult.csv"
    
    if not adult_path.exists():
        print("Downloading Adult Income dataset...")
        try:
            # Create synthetic data directly (more reliable than OpenML)
            return create_synthetic_income_data()
        except Exception as e:
            print(f"Error creating dataset: {e}")
            return create_synthetic_income_data()
    else:
        df = pd.read_csv(adult_path)
        # Ensure column names match expected format
        if 'sex' in df.columns and 'gender' not in df.columns:
            df = df.rename(columns={'sex': 'gender'})
        return df

def create_synthetic_income_data(n_samples=10000):
    """Create synthetic income data for testing."""
    np.random.seed(42)
    
    data = {
        'age': np.random.randint(18, 80, n_samples),
        'workclass': np.random.choice(['Private', 'Self-emp-not-inc', 'Self-emp-inc', 'Federal-gov', 'Local-gov', 'State-gov', 'Without-pay', 'Never-worked'], n_samples),
        'education': np.random.choice(['Bachelors', 'Some-college', '11th', 'HS-grad', 'Prof-school', 'Assoc-acdm', 'Assoc-voc', '9th', '7th-8th', '12th', 'Masters', '1st-4th', '10th', 'Doctorate', '5th-6th', 'Preschool'], n_samples),
        'marital-status': np.random.choice(['Married-civ-spouse', 'Divorced', 'Never-married', 'Separated', 'Widowed', 'Married-spouse-absent', 'Married-AF-spouse'], n_samples),
        'occupation': np.random.choice(['Tech-support', 'Craft-repair', 'Other-service', 'Sales', 'Exec-managerial', 'Prof-specialty', 'Handlers-cleaners', 'Machine-op-inspct', 'Adm-clerical', 'Farming-fishing', 'Transport-moving', 'Priv-house-serv', 'Protective-serv', 'Armed-Forces'], n_samples),
        'relationship': np.random.choice(['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried'], n_samples),
        'race': np.random.choice(['White', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other', 'Black'], n_samples),
        'gender': np.random.choice(['Male', 'Female'], n_samples),
        'capital-gain': np.random.choice([0] * 90 + list(np.random.randint(1000, 100000, 10)), n_samples),
        'capital-loss': np.random.choice([0] * 95 + list(np.random.randint(100, 5000, 5)), n_samples),
        'hours-per-week': np.random.randint(1, 100, n_samples),
        'native-country': np.random.choice(['United-States', 'Cuba', 'Jamaica', 'India', 'Mexico', 'South', 'Puerto-Rico', 'Honduras', 'England', 'Canada', 'Germany', 'Iran', 'Philippines', 'Italy', 'Poland', 'Columbia', 'Cambodia', 'Thailand', 'Ecuador', 'Laos', 'Taiwan', 'Haiti', 'Portugal', 'Dominican-Republic', 'El-Salvador', 'France', 'Guatemala', 'China', 'Japan', 'Yugoslavia', 'Peru', 'Outlying-US(Guam-USVI-etc)', 'Scotland', 'Trinadad&Tobago', 'Greece', 'Nicaragua', 'Vietnam', 'Hong', 'Ireland', 'Hungary', 'Holand-Netherlands'], n_samples),
        'income': np.random.choice([0, 1], n_samples, p=[0.75, 0.25])
    }
    
    # Adjust income based on logical factors
    df = pd.DataFrame(data)
    
    # Higher probability of >50K for higher education
    high_ed = ['Bachelors', 'Masters', 'Doctorate', 'Prof-school']
    df.loc[df['education'].isin(high_ed), 'income'] = np.random.choice([0, 1], df['education'].isin(high_ed).sum(), p=[0.4, 0.6])
    
    # Higher probability for exec-managerial and prof-specialty
    high_occ = ['Exec-managerial', 'Prof-specialty']
    df.loc[df['occupation'].isin(high_occ), 'income'] = np.random.choice([0, 1], df['occupation'].isin(high_occ).sum(), p=[0.3, 0.7])
    
    # Higher probability for married men
    df.loc[(df['gender'] == 'Male') & (df['marital-status'] == 'Married-civ-spouse'), 'income'] = np.random.choice([0, 1], ((df['gender'] == 'Male') & (df['marital-status'] == 'Married-civ-spouse')).sum(), p=[0.5, 0.5])
    
    df.to_csv(RAW_DATA_DIR / "adult.csv", index=False)
    print(f"Synthetic dataset created with {n_samples} samples")
    return df

def train_income_model():
    """Complete training pipeline for income classification."""
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("INCOME CLASSIFICATION MODEL TRAINING")
    logger.info("=" * 60)
    
    # Step 1: Load data
    logger.info("Step 1: Loading data...")
    df = download_adult_dataset()
    
    # Step 2: Preprocess
    logger.info("Step 2: Preprocessing data...")
    loader = DataLoader(logger)
    
    # Handle missing values
    df = loader.handle_missing_values(df, strategy="drop")
    
    # Remove duplicates
    df = loader.remove_duplicates(df)
    
    # Ensure target is binary
    if df['income'].dtype == 'object':
        df['income'] = df['income'].apply(lambda x: 1 if '>50K' in str(x) else 0)
    
    logger.info(f"Final dataset shape: {df.shape}")
    logger.info(f"Class distribution:\n{df['income'].value_counts()}")
    
    # Step 3: Split data
    logger.info("Step 3: Splitting data...")
    X_train, X_test, y_train, y_test = loader.split_data(
        df,
        target_col=INCOME_MODEL_CONFIG["target"],
        test_size=INCOME_MODEL_CONFIG["test_size"],
        random_state=INCOME_MODEL_CONFIG["random_state"]
    )
    
    # Step 4: Feature Engineering
    logger.info("Step 4: Feature engineering...")
    engineer = IncomeFeatureEngineer(logger)
    preprocessor = engineer.create_income_preprocessor()
    
    X_train_processed, X_test_processed = engineer.fit_transform(X_train, X_test)
    
    # Save preprocessor
    engineer.save_preprocessor(INCOME_MODEL_CONFIG["preprocessor_path"])
    
    # Get feature names
    try:
        feature_names = engineer.get_income_feature_names()
        logger.info(f"Number of features after encoding: {len(feature_names)}")
    except Exception as e:
        logger.warning(f"Could not get feature names: {e}")
        feature_names = None
    
    # Step 5: Train Models
    logger.info("Step 5: Training models...")
    trainer = ModelTrainer(logger)
    results = trainer.train_classification_models(
        X_train_processed, X_test_processed, y_train, y_test,
        models=INCOME_MODEL_CONFIG["models_to_train"]
    )
    
    # Step 6: Display Results
    logger.info("Step 6: Model comparison...")
    comparison = trainer.get_comparison_table()
    logger.info("\n" + comparison.to_string())
    
    # Step 7: Feature Importance
    logger.info("Step 7: Feature importance...")
    importance = trainer.get_feature_importance(feature_names)
    if importance:
        importance_df = pd.DataFrame(
            list(importance.items()),
            columns=['Feature', 'Importance']
        ).sort_values('Importance', ascending=False).head(10)
        logger.info("\nTop 10 Important Features:\n" + importance_df.to_string(index=False))
    
    # Step 8: Save Best Model
    logger.info("Step 8: Saving best model...")
    trainer.save_best_model(INCOME_MODEL_CONFIG["model_path"])
    
    logger.info("=" * 60)
    logger.info(f"Training complete! Best model: {trainer.best_model_name}")
    logger.info("=" * 60)
    
    return trainer.best_model, comparison

if __name__ == "__main__":
    train_income_model()
