#!/usr/bin/env python
"""Script to train the salary prediction model."""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.pipelines.train_salary_model import train_salary_model

def main():
    """Train salary model."""
    print("=" * 80)
    print("SMART SALARY PREDICTOR - MODEL TRAINING")
    print("=" * 80)
    print()
    
    # Train salary regression model
    print("Training Salary Regression Model...")
    print("-" * 80)
    try:
        salary_model, salary_comparison = train_salary_model()
        print("✅ Salary model trained successfully!")
    except Exception as e:
        print(f"❌ Error training salary model: {e}")
    
    print()
    print("=" * 80)
    print("TRAINING COMPLETE!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  1. Start the backend: uvicorn backend.main:app --reload")
    print("  2. Start the dashboard: streamlit run dashboard/app.py")
    print()

if __name__ == "__main__":
    main()
