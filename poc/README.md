# QuizFusion POC - Proof of Concept

This is a proof-of-concept for the modernized QuizFusion test creation interface.

## 🚀 Quick Start (One Command!)

```bash
cd poc
python run.py
```

Or even simpler:
```bash
./poc/start.sh
```

That's it! Your browser will open automatically.

## Features Demonstrated

- **Three Editor Modes**: Visual, Hybrid (code + visual), and Code
- **Python Code Execution**: Run Python code to generate dynamic problems
- **Live Preview**: See rendered output with variable substitution
- **Problem Bank**: Simple database of reusable problems
- **Variable Namespace**: Share variables between code and templates

## Running the POC

### Single Command (Recommended)

```bash
cd poc
python run.py
```

This will:
- Install dependencies if needed
- Start the backend server (port 8000)
- Start the frontend server (port 8080)
- Open your browser automatically
- Press Ctrl+C to stop everything

### Manual Start (Alternative)

If you prefer to run servers separately:

```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
python -m http.server 8080
```

Then visit: http://localhost:8080

## Architecture

```
poc/
├── backend/
│   ├── main.py           # FastAPI app
│   ├── models.py         # Data models
│   ├── database.py       # SQLite database
│   └── executor.py       # Python code execution engine
├── frontend/
│   ├── index.html        # Main UI
│   ├── app.js            # JavaScript logic
│   └── styles.css        # Styling
└── database/
    └── problems.db       # SQLite database (created on first run)
```

## Key Endpoints

- `GET /api/problems` - List all problems
- `GET /api/problems/{id}` - Get specific problem
- `POST /api/problems` - Create new problem
- `PUT /api/problems/{id}` - Update problem
- `DELETE /api/problems/{id}` - Delete problem
- `POST /api/execute` - Execute Python code and return namespace
- `POST /api/preview` - Generate preview with variable substitution
