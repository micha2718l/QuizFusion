"""
FastAPI backend for QuizFusion POC
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import json
import logging
from datetime import datetime

from models import (
    Problem, ProblemCreate, ProblemUpdate,
    CodeExecutionRequest, CodeExecutionResponse,
    PreviewRequest, PreviewResponse
)
from database import get_db, init_db, ProblemDB
from executor import CodeExecutor, substitute_variables

# Configure logging to file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backend.log'),
        logging.StreamHandler()  # Also print to console
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="QuizFusion POC API", version="0.1.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting QuizFusion POC API...")
    init_db()
    logger.info("Database initialized")

# Initialize code executor
executor = CodeExecutor()


@app.get("/")
async def root():
    logger.debug("Root endpoint accessed")
    return {
        "message": "QuizFusion POC API",
        "endpoints": {
            "problems": "/api/problems",
            "execute": "/api/execute",
            "preview": "/api/preview"
        }
    }


@app.get("/api/problems", response_model=List[Problem])
async def list_problems(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all problems"""
    logger.info(f"Listing problems (skip={skip}, limit={limit})")
    problems = db.query(ProblemDB).offset(skip).limit(limit).all()
    logger.debug(f"Found {len(problems)} problems")
    
    # Convert to Pydantic models
    result = []
    for p in problems:
        problem_dict = {
            'id': p.id,
            'type': p.type,
            'mode': p.mode,
            'statement': p.statement,
            'setup_code': p.setup_code,
            'choices': json.loads(p.choices) if p.choices else None,
            'questions': json.loads(p.questions) if p.questions else None,
            'extras': json.loads(p.extras) if p.extras else None,
            'tags': json.loads(p.tags) if p.tags else [],
            'difficulty': p.difficulty,
            'topic': p.topic,
            'created_at': p.created_at,
            'updated_at': p.updated_at,
            'usage_count': p.usage_count
        }
        result.append(Problem(**problem_dict))
    
    return result


@app.get("/api/problems/{problem_id}", response_model=Problem)
async def get_problem(problem_id: int, db: Session = Depends(get_db)):
    """Get a specific problem by ID"""
    logger.info(f"Getting problem {problem_id}")
    problem = db.query(ProblemDB).filter(ProblemDB.id == problem_id).first()
    if not problem:
        logger.warning(f"Problem {problem_id} not found")
        raise HTTPException(status_code=404, detail="Problem not found")
    
    logger.debug(f"Problem {problem_id} found: {problem.statement[:50]}...")
    problem_dict = {
        'id': problem.id,
        'type': problem.type,
        'mode': problem.mode,
        'statement': problem.statement,
        'setup_code': problem.setup_code,
        'choices': json.loads(problem.choices) if problem.choices else None,
        'questions': json.loads(problem.questions) if problem.questions else None,
        'extras': json.loads(problem.extras) if problem.extras else None,
        'tags': json.loads(problem.tags) if problem.tags else [],
        'difficulty': problem.difficulty,
        'topic': problem.topic,
        'created_at': problem.created_at,
        'updated_at': problem.updated_at,
        'usage_count': problem.usage_count
    }
    
    return Problem(**problem_dict)


@app.post("/api/problems", response_model=Problem)
async def create_problem(problem: ProblemCreate, db: Session = Depends(get_db)):
    """Create a new problem"""
    logger.info(f"Creating new problem: type={problem.type}, mode={problem.mode}")
    db_problem = ProblemDB(
        type=problem.type,
        mode=problem.mode,
        statement=problem.statement,
        setup_code=problem.setup_code,
        choices=json.dumps(problem.choices) if problem.choices else None,
        questions=json.dumps(problem.questions) if problem.questions else None,
        extras=json.dumps(problem.extras) if problem.extras else None,
        tags=json.dumps(problem.tags),
        difficulty=problem.difficulty,
        topic=problem.topic
    )
    
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    
    logger.info(f"Problem created with id={db_problem.id}")
    return await get_problem(db_problem.id, db)


@app.put("/api/problems/{problem_id}", response_model=Problem)
async def update_problem(
    problem_id: int,
    problem: ProblemUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing problem"""
    logger.info(f"Updating problem {problem_id}")
    db_problem = db.query(ProblemDB).filter(ProblemDB.id == problem_id).first()
    if not db_problem:
        logger.warning(f"Problem {problem_id} not found for update")
        raise HTTPException(status_code=404, detail="Problem not found")
    
    # Update fields
    db_problem.type = problem.type
    db_problem.mode = problem.mode
    db_problem.statement = problem.statement
    db_problem.setup_code = problem.setup_code
    db_problem.choices = json.dumps(problem.choices) if problem.choices else None
    db_problem.questions = json.dumps(problem.questions) if problem.questions else None
    db_problem.extras = json.dumps(problem.extras) if problem.extras else None
    db_problem.tags = json.dumps(problem.tags)
    db_problem.difficulty = problem.difficulty
    db_problem.topic = problem.topic
    
    db.commit()
    db.refresh(db_problem)
    
    return await get_problem(db_problem.id, db)


@app.delete("/api/problems/{problem_id}")
async def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    """Delete a problem"""
    logger.info(f"Deleting problem {problem_id}")
    db_problem = db.query(ProblemDB).filter(ProblemDB.id == problem_id).first()
    if not db_problem:
        logger.warning(f"Problem {problem_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Problem not found")
    
    db.delete(db_problem)
    db.commit()
    
    logger.info(f"Problem {problem_id} deleted successfully")
    return {"message": "Problem deleted successfully"}


@app.post("/api/execute", response_model=CodeExecutionResponse)
async def execute_code(request: CodeExecutionRequest):
    """Execute Python code and return namespace"""
    logger.info(f"Executing code: {len(request.code)} characters")
    logger.debug(f"Code to execute:\n{request.code}")
    
    success, namespace, output, figures = executor.execute(request.code, seed=None)
    
    logger.info(f"Code execution {'succeeded' if success else 'failed'}")
    if not success:
        logger.error(f"Execution error: {output}")
    else:
        logger.debug(f"Namespace keys: {list(namespace.keys())}")
    
    return CodeExecutionResponse(
        success=success,
        namespace=namespace,
        error=output if not success else None,
        figures=figures
    )


@app.post("/api/preview", response_model=PreviewResponse)
async def preview_problem(request: PreviewRequest):
    """Generate a preview of the problem with variable substitution"""
    logger.info(f"Generating preview for problem type={request.problem.type}, mode={request.problem.mode}")
    try:
        # Execute setup code if present
        namespace = {}
        if request.problem.setup_code and request.problem.mode in ['hybrid', 'code']:
            logger.debug(f"Executing setup code for preview")
            success, namespace, output, figures = executor.execute(
                request.problem.setup_code,
                seed=request.seed
            )
            
            if not success:
                logger.error(f"Setup code execution failed: {output}")
                return PreviewResponse(
                    html="",
                    namespace={},
                    error=f"Code execution error:\n{output}"
                )
            logger.debug(f"Setup code executed, namespace keys: {list(namespace.keys())}")
        
        # Substitute variables in statement
        statement = substitute_variables(request.problem.statement, namespace)
        
        # Build HTML preview
        html = f"<div class='problem-preview'>"
        html += f"<h3>Problem Statement</h3>"
        html += f"<p>{statement}</p>"
        
        # Add choices for multiple choice
        if request.problem.type == 'multiple_choice' and request.problem.choices:
            html += "<h4>Choices:</h4><ol type='a'>"
            for choice in request.problem.choices:
                correct_class = " class='correct'" if choice.correct else ""
                html += f"<li{correct_class}>{choice.statement}</li>"
            html += "</ol>"
        
        # Add questions for work problems
        if request.problem.type == 'work' and request.problem.questions:
            html += "<h4>Questions:</h4>"
            for i, question in enumerate(request.problem.questions, 1):
                q_statement = substitute_variables(question.statement, namespace)
                html += f"<div class='question'>"
                html += f"<p><strong>Question {i}</strong> ({question.points} points)</p>"
                html += f"<p>{q_statement}</p>"
                if question.answer_code and question.answer_code in namespace:
                    answer_value = namespace[question.answer_code]
                    if isinstance(answer_value, dict) and '_type' in answer_value:
                        answer_str = answer_value.get('formatted', str(answer_value))
                    else:
                        answer_str = str(answer_value)
                    html += f"<p><em>Answer: {answer_str}</em></p>"
                html += f"<div class='answer-space' style='height: {question.space * 1.5}em;'></div>"
                html += "</div>"
        
        html += "</div>"
        
        logger.info(f"Preview generated successfully, HTML length: {len(html)} chars")
        return PreviewResponse(
            html=html,
            namespace=namespace,
            error=None
        )
        
    except Exception as e:
        logger.exception(f"Preview generation error: {str(e)}")
        return PreviewResponse(
            html="",
            namespace={},
            error=f"Preview generation error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
