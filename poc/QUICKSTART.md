# QuizFusion POC - Quick Start Guide

## What We've Built

A proof-of-concept demonstrating the modernized QuizFusion interface with:

✅ **Three Editor Modes**
- Visual: Simple form-based (no code)
- Hybrid: Python code + visual editor (RECOMMENDED)
- Code: Full Python like current notebooks

✅ **Live Features**
- Real-time preview with variable substitution
- Python code execution in browser
- Dynamic problem generation with random values
- Matplotlib figure support
- Problem bank with CRUD operations

✅ **Sample Problems Included**
- Multiple choice with dynamic variables
- Work problems with calculated answers
- Physics problems using Value/Unit classes

## Running the POC

### One Command to Rule Them All! 🚀

```bash
cd /Users/mjhaas/code/QuizFusion/poc
python run.py
```

That's it! The launcher will:
- ✓ Check and install dependencies
- ✓ Start the backend server (port 8000)
- ✓ Start the frontend server (port 8080)  
- ✓ Open your browser automatically

Press **Ctrl+C** when you're done to stop everything cleanly.

### Manual Start (If You Prefer)

```bash
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend
cd frontend
python -m http.server 8080
```

Then open your browser to: **http://localhost:8080**

## Tour of the Interface

### Left Sidebar: Problem Bank
- Lists all saved problems
- Click to load and edit
- "New Problem" button creates fresh problem

### Main Panel: Editor
- **Mode tabs**: Switch between Visual/Hybrid/Code
- **Problem Type**: Multiple choice, Work, Bonus, Information
- **Metadata**: Tags, topic, difficulty
- **Setup Code** (Hybrid/Code mode): Python code for variables
- **Statement**: Problem text with `{variable}` placeholders
- **Choices/Questions**: Type-specific fields

### Right Panel: Preview
- Live preview of rendered problem
- Shows variable substitution in action
- "Refresh" button updates preview
- Variables display shows computed values

## Try These Examples

### Example 1: Static Multiple Choice (Visual Mode)
1. Click "New Problem"
2. Keep mode as "Visual"
3. Type: "Multiple Choice"
4. Statement: "What is 2 + 2?"
5. Add choices: 3, 4 (mark correct), 5, 6
6. See preview update automatically
7. Click "Save Problem"

### Example 2: Dynamic Spring Problem (Hybrid Mode)
1. Click "New Problem"
2. Switch to "Hybrid" mode
3. Type: "Work Problem"
4. Setup Code:
```python
import numpy as np
from quizfusion.stuff import Value

mass = Value(np.random.uniform(3, 8), 'kg')
spring_k = Value(np.random.uniform(200, 500), 'N/m')
compression = Value(0.2, 'm')
max_speed = compression * np.sqrt(spring_k / mass)
```

5. Statement: "A box of mass {mass} is pushed against a spring with constant {spring_k}..."
6. Add question: "What is the maximum speed?"
7. Click "Run Code" to execute
8. See variables populate in preview
9. Save and regenerate with different random values!

### Example 3: Browse Existing Problems
1. Look at the 3 sample problems in the sidebar
2. Click each to see different modes
3. Edit and save changes
4. Note how Hybrid mode combines code + visual

## Key Features to Test

### Code Execution
- Click "Run Code" to execute Python
- See namespace variables extracted
- Errors show with helpful messages

### Variable Substitution
- Use `{variable_name}` in statements
- Variables from code automatically replaced
- Works with Value objects (shows units!)

### Live Preview
- Type in statement field
- Preview updates automatically (500ms debounce)
- Shows formatted output with proper styling

### Problem Bank
- All problems saved to SQLite database
- Persistent across sessions
- Click to load and edit

## Architecture Highlights

```
Frontend (port 8080)
    ↓ HTTP requests
Backend (port 8000)
    ↓ Executes Python
Code Executor
    ↓ Extracts namespace
Database (SQLite)
```

## Next Steps

This POC demonstrates the core workflow. To make it production-ready:

1. **Add more features**:
   - Drag-drop test builder
   - Image upload
   - LaTeX rendering (KaTeX included but not wired up)
   - Export to PDF/HTML
   - Search and filter in problem bank

2. **Improve code execution**:
   - Better sandboxing (RestrictedPython)
   - Timeout handling
   - Memory limits

3. **Polish UI**:
   - Better error messages
   - Keyboard shortcuts
   - Undo/redo
   - Auto-save drafts

4. **Add collaboration**:
   - User accounts
   - Sharing problems
   - Version history

## Feedback Requested

Please test and provide feedback on:
- Is the three-mode approach intuitive?
- Does Hybrid mode feel natural?
- Is the preview helpful?
- What features are missing?
- Any UI/UX improvements?

## Troubleshooting

**Backend won't start**: Make sure you're in the `poc/backend` directory and have installed dependencies

**Frontend shows errors**: Check that backend is running on port 8000

**Code won't execute**: Verify quizfusion package is installed (`pip install -e .` from project root)

**Database issues**: Delete `poc/database/problems.db` to reset with sample data

## Code Structure

```
poc/
├── backend/
│   ├── main.py          # FastAPI app, endpoints
│   ├── models.py        # Pydantic data models
│   ├── database.py      # SQLAlchemy ORM
│   └── executor.py      # Python code execution
├── frontend/
│   ├── index.html       # UI structure
│   ├── styles.css       # Styling
│   └── app.js           # JavaScript logic
└── database/
    └── problems.db      # SQLite (created on first run)
```
