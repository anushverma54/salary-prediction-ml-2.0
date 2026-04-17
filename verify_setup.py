#!/usr/bin/env python
"""Verify project setup and dependencies."""
import sys
from pathlib import Path

def check_python_version():
    """Check Python version."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    print("\nChecking Python dependencies...")
    
    required = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'sklearn': 'scikit-learn',
        'joblib': 'joblib',
        'plotly': 'plotly',
        'streamlit': 'Streamlit',
        'requests': 'requests'
    }
    
    all_ok = True
    for module, name in required.items():
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} (Not installed)")
            all_ok = False
    
    return all_ok

def check_project_structure():
    """Check project structure."""
    print("\nChecking project structure...")
    
    base_path = Path(__file__).parent
    
    required_dirs = [
        'configs',
        'data/raw',
        'data/processed',
        'src/data',
        'src/features',
        'src/models',
        'src/pipelines',
        'src/visualization',
        'src/utils',
        'backend',
        'frontend/react-app',
        'dashboard',
        'artifacts',
        'tests'
    ]
    
    all_ok = True
    for dir_path in required_dirs:
        full_path = base_path / dir_path
        if full_path.exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ (Missing)")
            all_ok = False
    
    return all_ok

def check_key_files():
    """Check key files."""
    print("\nChecking key files...")
    
    base_path = Path(__file__).parent
    
    required_files = [
        'requirements.txt',
        'README.md',
        'backend/main.py',
        'src/pipelines/train_income_model.py',
        'src/pipelines/train_salary_model.py',
        'dashboard/dashboard.py',
        'frontend/react-app/package.json',
        'frontend/react-app/src/App.js'
    ]
    
    all_ok = True
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (Missing)")
            all_ok = False
    
    return all_ok

def check_models_trained():
    """Check if models are trained."""
    print("\nChecking trained models...")
    
    base_path = Path(__file__).parent
    artifacts_dir = base_path / 'artifacts'
    
    income_model = artifacts_dir / 'income_model.pkl'
    salary_model = artifacts_dir / 'salary_model.pkl'
    
    if income_model.exists():
        print("✅ Income classification model trained")
    else:
        print("❌ Income classification model (Not trained - Run: python train_all.py)")
    
    if salary_model.exists():
        print("✅ Salary regression model trained")
    else:
        print("❌ Salary regression model (Not trained - Run: python train_all.py)")
    
    return income_model.exists() and salary_model.exists()

def check_npm():
    """Check if npm is available."""
    print("\nChecking npm availability...")
    import shutil
    
    if shutil.which('npm'):
        print("✅ npm is available")
        return True
    else:
        print("❌ npm not found (Required for frontend)")
        return False

def main():
    """Run all checks."""
    print("=" * 80)
    print("SALARY PREDICTOR - SETUP VERIFICATION")
    print("=" * 80)
    print()
    
    results = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'Project Structure': check_project_structure(),
        'Key Files': check_key_files(),
        'npm': check_npm(),
    }
    
    models_trained = check_models_trained()
    
    print()
    print("=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    print()
    
    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check:<25} {status}")
    
    print(f"{'Models Trained':<25} {'✅ PASS' if models_trained else '⚠️  NEED TRAINING'}")
    
    print()
    
    all_passed = all(results.values())
    
    if all_passed and models_trained:
        print("🎉 Setup is complete! You can start the services:")
        print("   python start_all.py")
    elif all_passed and not models_trained:
        print("⚠️  Setup is ready but models need training:")
        print("   python train_all.py")
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
        print("\nTo install dependencies:")
        print("   pip install -r requirements.txt")
    
    print()

if __name__ == "__main__":
    main()
