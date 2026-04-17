"""Training pipeline for Salary Regression Model."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from src.data.data_loader import DataLoader
from src.features.feature_engineering import SalaryFeatureEngineer
from src.models.model_trainer import ModelTrainer
from src.utils.helpers import save_model, setup_logging
from configs.config import SALARY_MODEL_CONFIG, RAW_DATA_DIR, ARTIFACTS_DIR

def create_synthetic_salary_data(n_samples=25000):
    """Create synthetic salary data for testing."""
    np.random.seed(42)
    
    job_titles = ['Software Engineer', 'Data Scientist', 'Product Manager', 'DevOps Engineer', 
                  'UI/UX Designer', 'Marketing Manager', 'Sales Representative', 'HR Manager',
                  'Business Analyst', 'System Administrator', 'QA Engineer', 'Data Analyst',
                  'Full Stack Developer', 'Frontend Developer', 'Backend Developer', 'ML Engineer']
    
    education_levels = ['High School', 'Associate', 'Bachelor', 'Master', 'PhD', 'MBA']
    industries = ['Technology', 'Finance', 'Healthcare', 'Retail', 'Manufacturing', 'Education',
                  'Consulting', 'Media', 'Government', 'Energy']
    company_sizes = ['Startup (1-50)', 'Small (51-200)', 'Medium (201-1000)', 'Large (1000+)']
    locations = ['San Francisco', 'New York', 'Seattle', 'Austin', 'Boston', 'Chicago', 'Denver',
                 'Remote', 'Los Angeles', 'Washington DC', 'Atlanta', 'Dallas']
    remote_options = ['Fully Remote', 'Hybrid', 'On-site']
    certifications = ['None', 'AWS Certified', 'Google Cloud', 'Azure Certified', 'PMP', 
                     'Scrum Master', 'Data Science Cert', 'Cybersecurity Cert', 'Multiple']
    
    data = {
        'job_title': np.random.choice(job_titles, n_samples),
        'experience_years': np.random.randint(0, 25, n_samples),
        'education_level': np.random.choice(education_levels, n_samples),
        'skills_count': np.random.randint(1, 20, n_samples),
        'industry': np.random.choice(industries, n_samples),
        'company_size': np.random.choice(company_sizes, n_samples),
        'location': np.random.choice(locations, n_samples),
        'remote_work': np.random.choice(remote_options, n_samples),
        'certifications': np.random.choice(certifications, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Generate salary based on features (with some logic)
    base_salary = 40000
    
    # Job title multipliers
    title_multipliers = {
        'Software Engineer': 1.5, 'Data Scientist': 1.6, 'ML Engineer': 1.7,
        'DevOps Engineer': 1.5, 'Full Stack Developer': 1.45, 'Backend Developer': 1.4,
        'Frontend Developer': 1.3, 'Product Manager': 1.6, 'Data Analyst': 1.2,
        'Business Analyst': 1.1, 'Marketing Manager': 1.15, 'HR Manager': 1.0,
        'Sales Representative': 0.9, 'System Administrator': 1.1, 'QA Engineer': 1.05,
        'UI/UX Designer': 1.15
    }
    
    # Education multipliers
    edu_multipliers = {
        'High School': 1.0, 'Associate': 1.1, 'Bachelor': 1.25, 
        'Master': 1.4, 'PhD': 1.6, 'MBA': 1.5
    }
    
    # Location multipliers
    location_multipliers = {
        'San Francisco': 1.5, 'New York': 1.45, 'Seattle': 1.4, 'Boston': 1.35,
        'Washington DC': 1.3, 'Los Angeles': 1.3, 'Austin': 1.25, 'Denver': 1.15,
        'Chicago': 1.2, 'Atlanta': 1.1, 'Dallas': 1.15, 'Remote': 1.1
    }
    
    # Industry multipliers
    industry_multipliers = {
        'Technology': 1.4, 'Finance': 1.45, 'Consulting': 1.35, 'Healthcare': 1.2,
        'Energy': 1.25, 'Government': 1.0, 'Education': 0.85, 'Retail': 0.9,
        'Manufacturing': 0.95, 'Media': 1.1
    }
    
    # Company size multipliers
    size_multipliers = {
        'Startup (1-50)': 1.1, 'Small (51-200)': 1.05, 'Medium (201-1000)': 1.15,
        'Large (1000+)': 1.25
    }
    
    # Calculate base salary
    salaries = []
    for _, row in df.iterrows():
        salary = base_salary
        salary *= title_multipliers.get(row['job_title'], 1.0)
        salary *= edu_multipliers.get(row['education_level'], 1.0)
        salary *= location_multipliers.get(row['location'], 1.0)
        salary *= industry_multipliers.get(row['industry'], 1.0)
        salary *= size_multipliers.get(row['company_size'], 1.0)
        
        # Experience bonus (per year)
        salary += row['experience_years'] * 3500
        
        # Skills bonus
        salary += row['skills_count'] * 1500
        
        # Remote work adjustment
        if row['remote_work'] == 'Fully Remote':
            salary *= 1.05
        
        # Certification bonus
        if row['certifications'] != 'None':
            if row['certifications'] == 'Multiple':
                salary *= 1.15
            else:
                salary *= 1.08
        
        # Add random noise
        salary *= np.random.uniform(0.85, 1.15)
        
        salaries.append(int(salary))
    
    df['salary'] = salaries
    
    df.to_csv(RAW_DATA_DIR / "salary_data.csv", index=False)
    print(f"Synthetic salary dataset created with {n_samples} samples")
    return df

def train_salary_model():
    """Complete training pipeline for salary regression."""
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("SALARY REGRESSION MODEL TRAINING")
    logger.info("=" * 60)
    
    # Step 1: Load or create data
    logger.info("Step 1: Loading data...")
    salary_path = RAW_DATA_DIR / "salary_data.csv"
    
    if salary_path.exists():
        df = pd.read_csv(salary_path)
    else:
        df = create_synthetic_salary_data()
    
    logger.info(f"Dataset shape: {df.shape}")
    logger.info(f"Salary statistics:\n{df['salary'].describe()}")
    
    # Step 2: Preprocess
    logger.info("Step 2: Preprocessing data...")
    loader = DataLoader(logger)
    
    # Handle missing values
    df = loader.handle_missing_values(df, strategy="drop")
    
    # Remove duplicates
    df = loader.remove_duplicates(df)
    
    logger.info(f"Final dataset shape: {df.shape}")
    
    # Step 3: Split data
    logger.info("Step 3: Splitting data...")
    X_train, X_test, y_train, y_test = loader.split_data(
        df,
        target_col=SALARY_MODEL_CONFIG["target"],
        test_size=SALARY_MODEL_CONFIG["test_size"],
        random_state=SALARY_MODEL_CONFIG["random_state"]
    )
    
    # Step 4: Feature Engineering
    logger.info("Step 4: Feature engineering...")
    engineer = SalaryFeatureEngineer(logger)
    preprocessor = engineer.create_salary_preprocessor()
    
    X_train_processed, X_test_processed = engineer.fit_transform(X_train, X_test)
    
    # Save preprocessor
    engineer.save_preprocessor(SALARY_MODEL_CONFIG["preprocessor_path"])
    
    # Get feature names
    try:
        feature_names = engineer.get_salary_feature_names()
        logger.info(f"Number of features after encoding: {len(feature_names)}")
    except Exception as e:
        logger.warning(f"Could not get feature names: {e}")
        feature_names = None
    
    # Step 5: Train Models
    logger.info("Step 5: Training models...")
    trainer = ModelTrainer(logger)
    results = trainer.train_regression_models(
        X_train_processed, X_test_processed, y_train, y_test,
        models=SALARY_MODEL_CONFIG["models_to_train"]
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
    trainer.save_best_model(SALARY_MODEL_CONFIG["model_path"])
    
    logger.info("=" * 60)
    logger.info(f"Training complete! Best model: {trainer.best_model_name}")
    logger.info("=" * 60)
    
    return trainer.best_model, comparison

if __name__ == "__main__":
    train_salary_model()
