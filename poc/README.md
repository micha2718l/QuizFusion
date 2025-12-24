# QuizFusion POC - Proof of Concept

This is a proof-of-concept for the modernized QuizFusion test creation interface.

## Features Demonstrated

- **Three Editor Modes**: Visual, Hybrid (code + visual), and Code
- **Python Code Execution**: Run Python code to generate dynamic problems
- **Live Preview**: See rendered output with variable substitution
- **Problem Bank**: Simple database of reusable problems
- **Variable Namespace**: Share variables between code and templates

## Running the POC

### Install Dependencies

```bash
cd poc
pip install -r requirements.txt
```

### Start the Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Open the Frontend

Open `frontend/index.html` in your browser, or serve it:

```bash
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
