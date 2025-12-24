# QuizFusion POC - Single Command Launcher

Now you can start the entire POC with a single command!

## Quick Start

```bash
cd /Users/mjhaas/code/QuizFusion/poc
python run.py
```

That's it! The launcher will:
- ✅ Check and install dependencies automatically
- ✅ Start the backend server (port 8000)
- ✅ Start the frontend server (port 8080)
- ✅ Open your browser automatically to http://localhost:8080
- ✅ Show colored status messages
- ✅ Handle clean shutdown with Ctrl+C

## What You'll See

```
    ╔═══════════════════════════════════════════╗
    ║     🎓 QuizFusion POC Launcher 🚀        ║
    ╚═══════════════════════════════════════════╝
    
📦 Checking dependencies...
✓ All dependencies installed

🔧 Starting backend server...
   Waiting for backend to initialize...
✓ Backend running on http://localhost:8000

🌐 Starting frontend server...
✓ Frontend running on http://localhost:8080

🌍 Opening browser...

============================================================
✨ QuizFusion POC is running! ✨
============================================================

📍 Frontend: http://localhost:8080
📍 Backend API: http://localhost:8000
📍 API Docs: http://localhost:8000/docs

💡 Press Ctrl+C to stop the servers
```

## Stopping the Servers

Simply press **Ctrl+C** in the terminal:

```
🛑 Shutting down...
✓ Backend stopped
✓ Frontend stopped

👋 Thanks for using QuizFusion POC!
```

## Features of the Launcher

- **Dependency Management**: Automatically installs missing packages
- **Process Management**: Starts both servers and manages their lifecycle
- **Browser Integration**: Opens your default browser automatically
- **Error Handling**: Clear error messages if something goes wrong
- **Clean Shutdown**: Properly terminates all processes
- **Colored Output**: Easy-to-read status messages

## Alternative: Manual Start

If you prefer to run the servers separately:

**Backend:**
```bash
cd poc/backend
python main.py
```

**Frontend:**
```bash
cd poc/frontend
python -m http.server 8080
```

## Troubleshooting

**Port already in use:**
If you get an error about ports 8000 or 8080 being in use, stop any other services using those ports or modify the ports in `run.py`.

**Dependencies won't install:**
Try manually installing: `pip install -r poc/requirements.txt`

**Browser doesn't open:**
Manually navigate to http://localhost:8080

**Backend fails to start:**
Make sure you've installed the quizfusion package: `pip install -e .` from the project root

## Benefits of Single Command

- ✅ **Faster**: No need to open multiple terminals
- ✅ **Simpler**: One command to remember
- ✅ **Cleaner**: Everything starts and stops together
- ✅ **Better UX**: Automatic browser opening
- ✅ **Easy to share**: Simple instructions for others

## For Development

The launcher script (`run.py`) is fully customizable. You can modify:
- Port numbers
- Browser opening behavior
- Startup delay times
- Output messages

Just edit `poc/run.py` to suit your needs!
