# QuizFusion

A Python toolkit for generating, editing, and exporting quizzes, tests, and problem sets, with a focus on science and math content.

## Features

- **Notebook to PDF/HTML conversion:** Convert Jupyter notebooks containing quiz problems into styled PDFs or HTML files
- **Problem modeling:** Define multiple choice questions, work problems, and bonus questions with LaTeX/math rendering
- **Physical units support:** Handle scientific values with units for physics problems
- **Custom templates:** Use Jinja2 templates to customize the appearance of generated tests
- **Watch mode:** Automatically regenerate outputs when notebook files change

## Installation

1. Clone this repository
2. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Project Structure

```
QuizFusion/
├── quizfusion/           # Core package with problem models and conversion utilities
│   ├── testifyr.py      # Problem, question, and test class definitions
│   ├── stuff.py         # Physical units and values utilities
│   ├── utils.py         # General utility functions
│   ├── convert_utils.py # Notebook conversion functions
│   ├── out.py           # Output generation utilities
│   └── all_templates.py # Template management
├── notebooks/            # Jupyter notebooks with quiz definitions
│   ├── *.ipynb          # Example quiz/test notebooks
│   ├── testifyr.css     # CSS styling for rendered problems
│   └── temp/            # Temporary files (e.g., generated images)
├── scripts/              # CLI scripts and utilities
│   ├── test.py          # Main conversion script
│   ├── watch.py         # File watcher utility
│   ├── app.py           # Web application
│   └── hello.py         # Example script
├── templates/            # Jinja2 templates for output formatting
│   └── exam/            # Exam template files
├── web/                  # Web UI assets
│   └── essential/       # PyScript-based web applications
└── out/                  # Generated PDF and HTML files
```

## Usage

### Creating a Quiz Notebook

1. Create a new Jupyter notebook in the `notebooks/` directory
2. Import the necessary classes:
   ```python
   from testifyr import WorkProblem, Question, Test, MultipleChoiceProblem, Choice, Bonus
   from stuff import Value, Unit
   ```
3. Define your problems:
   ```python
   # Multiple choice problem
   mc = MultipleChoiceProblem(
       statement="What is the acceleration due to gravity on Earth?",
       choices=[
           Choice("9.8 m/s²", True),
           Choice("10 m/s²"),
           Choice("9.81 m/s"),
           Choice("98 m/s²")
       ]
   )
   
   # Work problem with multiple questions
   wp = WorkProblem(
       statement="A ball is thrown upward with initial velocity 20 m/s.",
       questions=[
           Question(statement="Calculate the maximum height reached.", space=5, points=4),
           Question(statement="What is the total time in the air?", space=5, points=3)
       ]
   )
   ```

### Converting Notebooks to PDF/HTML

Convert a notebook to HTML:
```bash
python scripts/test.py --file notebooks/your_notebook.ipynb --html
```

Convert to PDF:
```bash
python scripts/test.py --file notebooks/your_notebook.ipynb --pdf
```

Convert to both and enable watch mode:
```bash
python scripts/test.py --file notebooks/your_notebook.ipynb --pdf --html --watch
```

Output files will be generated in the `out/` directory.

## Development

The codebase has been reorganized into a proper Python package structure:
- Core logic is in the `quizfusion/` package
- CLI scripts are in the `scripts/` directory  
- Templates are in the `templates/` directory
- Symbolic links in `notebooks/` allow existing notebooks to continue working without modification

## Requirements

See `requirements.txt` for dependencies. Key requirements include:
- nbconvert
- nbformat
- matplotlib
- numpy
- IPython
- Jinja2
