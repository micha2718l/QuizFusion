# QuizFusion System Analysis & Modernization Plan

## Current System Understanding

### How It Works Now

#### 1. **Notebook-Based Test Creation**
- Instructors create Jupyter notebooks in `notebooks/` directory
- Each notebook contains Python code that defines test problems
- Import classes: `WorkProblem`, `Question`, `MultipleChoiceProblem`, `Choice`, `Bonus`, `Information`
- Import utilities: `Value`, `Unit` for handling physical quantities with units

#### 2. **Problem Types**
- **Multiple Choice Problems**: Statement + list of choices (one marked correct)
- **Work Problems**: Statement + list of questions (each with space for answers, points)
- **Bonus Problems**: Extra credit questions
- **Information**: Contextual info for groups of problems (not scored)

#### 3. **Key Features**
- **Variable substitution**: Problems use `Value` objects (e.g., `Value(9.81, 'm/s^2')`)
- **LaTeX rendering**: Math equations in statements and answers
- **Image support**: Matplotlib-generated figures or SVG diagrams
- **Custom units**: Can define unusual units (e.g., `'blark = 0.592 yard'`)
- **Dynamic calculations**: Problems can include computed values and validation

#### 4. **Workflow**
```
1. Create/edit notebook → 
2. Run cells to define problems → 
3. Create Test object with all problems → 
4. Run conversion script → 
5. Generate PDF/HTML with custom template
```

#### 5. **Template System**
- Jinja2 templates in `templates/exam/`
- Header with course info, date, student name fields
- CSS styling in `notebooks/testifyr.css`
- Configurable via `conf.json`

### Pain Points

1. **No GUI**: Must edit Python code directly in notebooks
2. **Technical barrier**: Requires Python/Jupyter knowledge (but code flexibility is ESSENTIAL)
3. **Manual process**: Run scripts manually after editing
4. **Limited reusability**: Hard to reuse/modify existing problems
5. **No problem bank**: No database or library of problems
6. **Version control challenges**: Notebooks are JSON, hard to diff
7. **No collaboration**: Can't easily share or review problems
8. **Image handling**: Must manually save/reference image files

**Critical Requirement**: Preserve the ability to write Python code for:
- Dynamic variable generation (random values, distributions)
- Complex calculations for answer keys
- Matplotlib figure generation
- Custom logic and validation
- Unit conversions and dimensional analysis

---

## Proposed Solution: Modern Test Creation System

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Web-Based Interface                      │
│  (React/Vue or PyScript for Python in browser)              │
│  • Visual problem editor                                     │
│  • Code editor (Monaco/CodeMirror with Python syntax)       │
│  • Live preview with variable substitution                   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                     API Layer (FastAPI)                      │
│  • CRUD operations for problems/tests                        │
│  • Code execution engine (sandboxed Python)                  │
│  • Rendering engine integration                              │
│  • Export to PDF/HTML                                        │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                 Code Execution Layer                         │
│  • Python interpreter (RestrictedPython or subprocess)       │
│  • Namespace management (extract variables from code)        │
│  • Auto-capture matplotlib figures                           │
│  • Import whitelist (numpy, matplotlib, quizfusion modules)  │
│  • Timeout and resource limits                               │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                   Data Layer (SQLite/JSON)                   │
│  • Problem bank (searchable, taggable)                       │
│    - Stores setup_code, statement, questions                 │
│  • Test definitions                                          │
│  • Template configurations                                   │
│  • Execution cache (for performance)                         │
└─────────────────────────────────────────────────────────────┘
```

### Core Features

#### 0. **Three Editor Modes (The Best of Both Worlds)**

**Visual Mode** - For simple, static problems:
- No code required
- Fill in forms for statement, choices/questions
- Fixed values for variables
- Use case: Basic multiple choice, straightforward problems

**Hybrid Mode** - For dynamic problems (RECOMMENDED):
- Python code block for setup/calculations
- Visual editor for statement with variable placeholders
- Code-generated values, figures, and answer keys
- Use case: Most physics problems with random values

**Code Mode** - For maximum flexibility:
- Full Python code like current notebooks
- Direct access to all classes (WorkProblem, Value, etc.)
- Can import any library, run any logic
- Use case: Complex multi-part problems, custom logic

**Example Workflow in Hybrid Mode:**

```python
# Setup Code (executed when problem is generated)
import numpy as np
from stuff import Value
import matplotlib.pyplot as plt

# Random parameters
angle = Value(np.random.uniform(15, 45), 'degree')
velocity = Value(np.random.uniform(20, 30), 'm/s')
mass = Value(np.random.uniform(0.1, 2.0), 'kg')

# Compute answer
v_x = velocity * np.cos(np.radians(angle.magnitude))
v_y = velocity * np.sin(np.radians(angle.magnitude))
time_flight = 2 * v_y / Value(9.81, 'm/s^2')
distance = v_x * time_flight

# Generate custom figure
fig, ax = plt.subplots()
t = np.linspace(0, time_flight.magnitude, 100)
x = v_x.magnitude * t
y = v_y.magnitude * t - 0.5 * 9.81 * t**2
ax.plot(x, y)
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Height (m)')
ax.grid(True)
# Figure automatically captured and inserted
```

Then in the visual editor:
- Statement: "A projectile is launched at {angle} with velocity {velocity}..."
- Question 1: "Calculate the horizontal distance" 
  - Answer: `{distance:.2f}` (auto-computed from code)
- Question 2: "What is the time of flight?"
  - Answer: `{time_flight:.2f}` (auto-computed from code)

**Code Execution Features:**
- ✅ Full Python environment (NumPy, Matplotlib, etc.)
- ✅ Access to existing Value/Unit classes
- ✅ Random value generation with constraints
- ✅ Complex calculations and validations
- ✅ Auto-capture matplotlib figures
- ✅ Namespace sharing between code and statement
- ✅ Error handling with helpful messages
- ✅ Sandboxed execution for safety

**Comparison: Same Problem in Three Modes**

*Problem: Spring compression with random values*

**Visual Mode (No Code):**
```
Statement: A box of mass 5.0 kg is pushed against a spring...
Variables:
  - mass: 5.0 kg
  - spring_k: 350 N/m
  - compression: 0.2 m
Questions:
  1. What is the maximum speed? (manual answer)
  2. Calculate the force (manual answer)
```

**Hybrid Mode (Recommended):**
```python
# Setup Code
import numpy as np
mass = Value(np.random.uniform(3, 8), 'kg')
spring_k = Value(np.random.uniform(200, 500), 'N/m')
compression = Value(0.2, 'm')
max_speed = compression * np.sqrt(spring_k/mass)
```
```
Statement: A box of mass {mass} is pushed against a spring 
           with spring constant {spring_k}...
Questions:
  1. What is the maximum speed? 
     Answer: {max_speed:.2f}  ← Auto-generated
  2. Calculate the force
     Answer: {spring_k * compression:.1f}  ← Auto-computed
```

**Code Mode (Maximum Flexibility):**
```python
# Full Python code, just like current notebooks
from testifyr import WorkProblem, Question
from stuff import Value
import numpy as np

mass = Value(np.random.uniform(3, 8), 'kg')
spring_k = Value(np.random.uniform(200, 500), 'N/m')
compression = Value(0.2, 'm')

statement = f"A box of mass {mass} is pushed against..."
questions = [
    Question(f"What is the maximum speed?", 
             space=10, 
             points=3,
             answer=f"v = {compression * np.sqrt(spring_k/mass):.2f}"),
    Question(f"Calculate the force", 
             space=10, 
             points=3,
             answer=f"F = {spring_k * compression:.1f}")
]
problem = WorkProblem(statement, questions)
```

**Key Insight:** Users can start with Visual mode, upgrade to Hybrid when they need randomness, and go to Code mode for complex multi-step problems. Each mode saves in a format that can be opened in the other modes (with some limitations).

#### 1. **Problem Editor Interface**

**Dual-Mode Editor: Visual + Code**

Users can toggle between three modes:
- **Visual Mode** (beginner-friendly, no code)
- **Hybrid Mode** (visual + code snippets)
- **Code Mode** (full Python code, like current notebooks)

**Layout (Hybrid Mode):**
```
┌──────────────────────────────────────────────────────────────┐
│ [Problem Type ▼] [Tags: physics, energy, ...]  [Save] [Del]│
│ Mode: [Visual] [Hybrid] [Code]                              │
├──────────────────────────────────────────────────────────────┤
│ Setup Code (Python):                      [▶ Run] [Variables]│
│ ┌────────────────────────────────────────────────────────┐  │
│ │ import numpy as np                                      │  │
│ │ from stuff import Value                                 │  │
│ │                                                         │  │
│ │ # Define variables                                      │  │
│ │ mass = Value(np.random.uniform(3, 8), 'kg')           │  │
│ │ spring_k = Value(np.random.uniform(200, 500), 'N/m')  │  │
│ │ compression = Value(0.2, 'm')                          │  │
│ │                                                         │  │
│ │ # Calculations for answer key                           │  │
│ │ max_speed = compression * np.sqrt(spring_k/mass)       │  │
│ │ energy = 0.5 * spring_k * compression**2               │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                              │
│ Statement:                                                    │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ A box of mass {mass} is pushed against a spring with   │  │
│ │ spring constant {spring_k} until compressed {compression}│
│ │                               [📷] [📐] [Insert Var ▼] │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                              │
│ Questions:                                                   │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ 1. What is the max speed? Points: 3 Space: 10 lines    │  │
│ │    Answer (computed): {max_speed:.2f}     [Code] [Hide]│  │
│ │                                                         │  │
│ │ 2. Draw a diagram  Points: 4 Space: 20 lines           │  │
│ │    Answer: (student work)                               │  │
│ │ [+ Add Question]                                        │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                              │
│ Preview (with current values):              [Regenerate]     │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ A box of mass 5.3 kg is pushed against a spring...     │  │
│ │ Answer: 1.47 m/s                                        │  │
│ └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

#### 2. **Rich Text Editor Features**

- **LaTeX support**: Inline math editor with preview
- **Variable insertion**: Dropdown to insert `{variable_name}` from code namespace
- **Image upload**: Drag-drop images, auto-base64 encode
- **Code-generated images**: Run matplotlib code, auto-insert figure
- **Drawing tools**: Simple diagram creator (optional)
- **Python code blocks**: Full syntax highlighting, execution, namespace sharing

#### 3. **Problem Bank**

```
┌──────────────────────────────────────────────────────────────┐
│ Problem Bank                                     [+ New]     │
├──────────────────────────────────────────────────────────────┤
│ Search: [___________] Tags: [all ▼] Type: [all ▼]           │
├──────────────────────────────────────────────────────────────┤
│ ☐ Projectile motion - basic                     [Edit] [Del]│
│   Tags: kinematics, projectile                               │
│   Last used: 2024-12-01                                      │
├──────────────────────────────────────────────────────────────┤
│ ☐ Energy conservation - spring                  [Edit] [Del]│
│   Tags: energy, springs, conservation                        │
│   Last used: 2024-11-15                                      │
├──────────────────────────────────────────────────────────────┤
│ ☐ Momentum collision - elastic                  [Edit] [Del]│
│   Tags: momentum, collisions                                 │
│   Last used: Never                                           │
└──────────────────────────────────────────────────────────────┘
```

#### 4. **Test Builder**

```
┌──────────────────────────────────────────────────────────────┐
│ Test: Physics Final Exam 2025                   [Export PDF]│
├──────────────────────────────────────────────────────────────┤
│ Multiple Choice Section                                      │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ 1. Energy conservation basics          [↑] [↓] [×]     │  │
│ │ 2. Momentum collision types            [↑] [↓] [×]     │  │
│ │ [+ Add from Bank] [+ Create New]                       │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                              │
│ Work Problems Section                                        │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ 1. Spring compression problem          [↑] [↓] [×]     │  │
│ │ 2. Projectile motion                   [↑] [↓] [×]     │  │
│ │ [+ Add from Bank] [+ Create New]                       │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                              │
│ Bonus Section                                                │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ 1. Betelgeuse energy calculation       [↑] [↓] [×]     │  │
│ │ [+ Add from Bank] [+ Create New]                       │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                              │
│ Total Points: 45 + 3 bonus                                   │
└──────────────────────────────────────────────────────────────┘
```

#### 5. **Template Configuration**

```
┌──────────────────────────────────────────────────────────────┐
│ Test Header Configuration                                    │
├──────────────────────────────────────────────────────────────┤
│ Test Title: [Final Exam                                   ]  │
│ Course: [PHYS 1061 H002                                   ]  │
│ Instructor: [Michael Haas                                 ]  │
│                                                              │
│ Include on test:                                             │
│ ☑ Date field     ☑ Student name field                       │
│ ☑ Class number   ☑ Instructions                             │
│                                                              │
│ Instructions:                                                │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Please read and follow all instructions carefully...   │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                              │
│ Logo: [Upload] [Remove] [Preview]                           │
└──────────────────────────────────────────────────────────────┘
```

### Technical Stack Recommendations

#### Option 1: Web-Based (Recommended)
- **Frontend**: React + TipTap (rich text) + KaTeX (math)
- **Backend**: FastAPI (Python API)
- **Database**: SQLite + SQLAlchemy ORM
- **Export**: Use existing nbconvert pipeline
- **Deploy**: Local Electron app or web server

**Pros:**
- Clean separation of concerns
- Can be hosted for team collaboration
- Mobile-friendly interface possible
- Easier testing and maintenance

#### Option 2: Python Desktop App
- **Framework**: PyQt6 or Tkinter
- **Rich text**: QTextEdit with custom formatting
- **Database**: SQLite
- **Export**: Direct integration with existing code

**Pros:**
- No web server needed
- Better offline support
- Tighter integration with existing Python code

#### Option 3: Hybrid (PyScript in Browser)
- **Frontend**: PyScript (Python in browser)
- **Backend**: Direct Python execution
- **Database**: Browser localStorage + export to JSON

**Pros:**
- Single-page app, no backend needed
- All Python, consistent language
- Can reuse existing classes directly

---

## Implementation Phases

### Phase 1: Foundation (2-3 weeks)
1. **Database schema design**
   - Problem table (type, statement, variables, questions, metadata)
   - Test table (title, metadata, problem_ids order)
   - Template table (header config, styling)

2. **API endpoints**
   - CRUD for problems
   - CRUD for tests
   - Export endpoint (notebook → PDF/HTML)

3. **Basic UI wireframes**
   - Problem list view
   - Problem editor (basic)

### Phase 2: Core Editor (3-4 weeks)
1. **Rich text editor**
   - LaTeX support
   - Variable placeholder system
   - Image upload/management

2. **Code execution engine**
   - Python interpreter integration (RestrictedPython or subprocess)
   - Namespace management and variable extraction
   - Auto-capture matplotlib figures
   - Error handling and debugging tools

3. **Variable system**
   - Define variables with units (visual mode)
   - Extract variables from code (hybrid/code mode)
   - Random value generation
   - Validation

4. **Problem types**
   - Multiple choice editor
   - Work problem with questions
   - Bonus/Information types
   - Code snippets for answer keys

### Phase 3: Test Builder (2 weeks)
1. **Test composition UI**
   - Drag-drop from problem bank
   - Reorder problems
   - Section organization

2. **Template configuration**
   - Header customization
   - Style options

3. **Export functionality**
   - Generate notebook from DB
   - Run existing conversion pipeline
   - Download PDF/HTML

### Phase 4: Advanced Features (2-3 weeks)
1. **Problem bank enhancements**
   - Search and filter
   - Tags and categories
   - Usage statistics

2. **Collaboration features**
   - Import/export problem sets
   - Version history
   - Comments/notes

3. **Quality of life**
   - Keyboard shortcuts
   - Templates for common problem types
   - Batch operations

---

## Data Models

### Problem Model
```python
@dataclass
class ProblemDefinition:
    id: str
    type: Literal['multiple_choice', 'work', 'bonus', 'information']
    
    # Code execution mode
    mode: Literal['visual', 'hybrid', 'code']  # NEW
    setup_code: Optional[str]  # Python code for variable generation
    
    # Statement and content
    statement: str  # Can include {variable} placeholders
    variables: List[Variable]  # [{name, value, unit, random_range}]
    metadata: Dict  # tags, difficulty, topic, author, created_date
    
    # Type-specific fields
    choices: Optional[List[Choice]]  # for multiple_choice
    questions: Optional[List[Question]]  # for work problems
    extras: Optional[List[str]]  # additional info
    figure: Optional[str]  # base64 or path
    figure_code: Optional[str]  # matplotlib code to generate figure
    
    # Computed fields
    points: int
    last_used: datetime
    usage_count: int
    
    # Execution context
    namespace: Dict[str, Any]  # Variables computed from setup_code

@dataclass
class Question:
    statement: str
    space: int  # lines of space for answer
    points: int
    answer_code: Optional[str]  # Python code to compute answer
    answer_static: Optional[str]  # Static answer text
```

### Test Model
```python
@dataclass
class TestDefinition:
    id: str
    title: str
    metadata: Dict  # course, instructor, date, etc.
    sections: List[Section]  # [{name, problem_ids, type}]
    template_config: Dict
    created_date: datetime
    last_modified: datetime
```

---

## Migration Strategy

### Backward Compatibility
1. Keep existing notebook workflow functional
2. Add import tool: notebook → database
3. Add export tool: database → notebook
4. Gradual migration of existing problems

### Import Existing Notebooks
```python
def import_notebook(notebook_path: str) -> List[ProblemDefinition]:
    """Parse existing notebook and extract problems to database"""
    # Execute notebook in isolated kernel
    # Extract problem objects from namespace
    # Convert to ProblemDefinition format
    # Save to database
```

---

## Next Steps

### Immediate Actions
1. **Choose tech stack** - Recommend Option 1 (Web-based)
2. **Design database schema** - Start with Problem and Test tables
3. **Create mockups** - UI designs for key screens
4. **Prototype editor** - Basic problem editor with LaTeX support

### Questions to Answer
1. Single-user or multi-user system?
2. Desktop app or web application?
3. Need for real-time collaboration?
4. Import priority: migrate all old notebooks or start fresh?
5. Mobile support required?

### Risk Mitigation
- Keep existing notebook system working during development
- Build import/export tools early
- Start with read-only problem bank, then add editing
- Incremental rollout with pilot users

---

## Estimated Timeline
- **Minimum Viable Product (MVP)**: 8-10 weeks
  - Problem bank (view/search)
  - Basic problem editor
  - Test builder
  - Export to PDF
  
- **Full System**: 12-16 weeks
  - All features
  - Polish and testing
  - Documentation
  - Migration tools

## Resource Requirements
- 1 full-stack developer (primary)
- 1 subject matter expert (instructor, part-time)
- UI/UX designer (optional, for polish)
