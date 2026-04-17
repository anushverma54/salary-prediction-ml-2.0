#!/usr/bin/env python
"""Script to start the Salary Prediction System (Backend + Streamlit)."""
import subprocess
import sys
import time
from pathlib import Path

def start_backend():
    """Start the FastAPI backend."""
    print("🚀 Starting FastAPI Backend on http://localhost:8000")
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--reload", "--port", "8000"],
        cwd=Path(__file__).parent
    )

def start_dashboard():
    """Start the Streamlit dashboard."""
    print("📊 Starting Streamlit Dashboard on http://localhost:8501")
    return subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "dashboard/app.py"],
        cwd=Path(__file__).parent
    )

def main():
    """Main function to start all services."""
    print("=" * 80)
    print("SMART SALARY PREDICTOR - STARTING SERVICES")
    print("=" * 80)
    print()
    
    processes = []
    
    try:
        # Start backend
        backend_proc = start_backend()
        processes.append(("Backend", backend_proc))
        time.sleep(3)
        
        # Start dashboard
        dashboard_proc = start_dashboard()
        processes.append(("Dashboard", dashboard_proc))
        
        print()
        print("=" * 80)
        print("✅ ALL SERVICES STARTED!")
        print("=" * 80)
        print()
        print("🔗 Access Points:")
        print("   • Dashboard (with Predictions): http://localhost:8501")
        print("   • API:                          http://localhost:8000")
        print("   • API Docs:                     http://localhost:8000/docs")
        print()
        print("⚠️  Press Ctrl+C to stop all services")
        print()
        
        # Wait for all processes
        while True:
            for name, proc in processes:
                if proc.poll() is not None:
                    print(f"❌ {name} process exited unexpectedly")
                    break
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping all services...")
        for name, proc in processes:
            print(f"   Stopping {name}...")
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except:
                proc.kill()
        print("✅ All services stopped")

if __name__ == "__main__":
    main()
