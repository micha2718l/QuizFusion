#!/usr/bin/env python3
"""
QuizFusion POC Launcher
Starts both backend and frontend servers with a single command
"""
import subprocess
import sys
import time
import webbrowser
from pathlib import Path
import signal
import os

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_colored(message, color=Colors.OKGREEN):
    print(f"{color}{message}{Colors.ENDC}")

def print_header():
    print_colored("""
    ╔═══════════════════════════════════════════╗
    ║     🎓 QuizFusion POC Launcher 🚀        ║
    ╚═══════════════════════════════════════════╝
    """, Colors.HEADER)

def check_dependencies():
    """Check if required packages are installed"""
    print_colored("📦 Checking dependencies...", Colors.OKCYAN)
    
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import pydantic
        print_colored("✓ All dependencies installed", Colors.OKGREEN)
        return True
    except ImportError as e:
        print_colored(f"✗ Missing dependency: {e.name}", Colors.FAIL)
        print_colored("Installing dependencies...", Colors.WARNING)
        
        poc_dir = Path(__file__).parent
        requirements = poc_dir / "requirements.txt"
        
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements)])
        print_colored("✓ Dependencies installed", Colors.OKGREEN)
        return True

def start_backend(poc_dir):
    """Start the FastAPI backend server"""
    print_colored("\n🔧 Starting backend server...", Colors.OKCYAN)
    
    backend_dir = poc_dir / "backend"
    env = os.environ.copy()
    env['PYTHONPATH'] = str(poc_dir.parent)
    
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=str(backend_dir),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Wait for backend to start
    print_colored("   Waiting for backend to initialize...", Colors.OKBLUE)
    time.sleep(3)
    
    if backend_process.poll() is None:
        print_colored("✓ Backend running on http://localhost:8000", Colors.OKGREEN)
        return backend_process
    else:
        print_colored("✗ Backend failed to start", Colors.FAIL)
        return None

def start_frontend(poc_dir):
    """Start the frontend HTTP server"""
    print_colored("\n🌐 Starting frontend server...", Colors.OKCYAN)
    
    frontend_dir = poc_dir / "frontend"
    
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8080"],
        cwd=str(frontend_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    time.sleep(1)
    
    if frontend_process.poll() is None:
        print_colored("✓ Frontend running on http://localhost:8080", Colors.OKGREEN)
        return frontend_process
    else:
        print_colored("✗ Frontend failed to start", Colors.FAIL)
        return None

def open_browser():
    """Open the application in the default browser"""
    print_colored("\n🌍 Opening browser...", Colors.OKCYAN)
    time.sleep(1)
    webbrowser.open("http://localhost:8080")

def cleanup(backend_process, frontend_process):
    """Clean up processes on exit"""
    print_colored("\n\n🛑 Shutting down...", Colors.WARNING)
    
    if backend_process and backend_process.poll() is None:
        backend_process.terminate()
        backend_process.wait(timeout=5)
        print_colored("✓ Backend stopped", Colors.OKGREEN)
    
    if frontend_process and frontend_process.poll() is None:
        frontend_process.terminate()
        frontend_process.wait(timeout=5)
        print_colored("✓ Frontend stopped", Colors.OKGREEN)
    
    print_colored("\n👋 Thanks for using QuizFusion POC!", Colors.HEADER)

def main():
    print_header()
    
    # Get POC directory
    poc_dir = Path(__file__).parent
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    backend_process = None
    frontend_process = None
    
    try:
        # Start backend
        backend_process = start_backend(poc_dir)
        if not backend_process:
            print_colored("\n❌ Failed to start backend. Check the error messages above.", Colors.FAIL)
            sys.exit(1)
        
        # Start frontend
        frontend_process = start_frontend(poc_dir)
        if not frontend_process:
            print_colored("\n❌ Failed to start frontend. Check the error messages above.", Colors.FAIL)
            cleanup(backend_process, None)
            sys.exit(1)
        
        # Open browser
        open_browser()
        
        # Print success message
        print_colored("\n" + "="*60, Colors.OKGREEN)
        print_colored("✨ QuizFusion POC is running! ✨", Colors.OKGREEN + Colors.BOLD)
        print_colored("="*60, Colors.OKGREEN)
        print_colored("\n📍 Frontend: http://localhost:8080", Colors.OKBLUE)
        print_colored("📍 Backend API: http://localhost:8000", Colors.OKBLUE)
        print_colored("📍 API Docs: http://localhost:8000/docs", Colors.OKBLUE)
        print_colored("📍 Backend Logs: poc/backend/backend.log", Colors.OKBLUE)
        print_colored("\n💡 Press Ctrl+C to stop the servers\n", Colors.WARNING)
        
        # Keep the script running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print_colored("\n❌ Backend process died unexpectedly!", Colors.FAIL)
                break
            if frontend_process.poll() is not None:
                print_colored("\n❌ Frontend process died unexpectedly!", Colors.FAIL)
                break
    
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print_colored(f"\n❌ Error: {e}", Colors.FAIL)
    finally:
        cleanup(backend_process, frontend_process)

if __name__ == "__main__":
    main()
