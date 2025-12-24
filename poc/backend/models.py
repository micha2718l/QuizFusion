"""
Data models for the QuizFusion POC
"""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class Variable(BaseModel):
    name: str
    value: Any
    unit: Optional[str] = None


class Choice(BaseModel):
    statement: str
    correct: bool = False


class Question(BaseModel):
    statement: str
    space: int = 10  # lines of space for answer
    points: int = 3
    answer_code: Optional[str] = None  # Python code to compute answer
    answer_static: Optional[str] = None  # Static answer text


class ProblemBase(BaseModel):
    type: Literal['multiple_choice', 'work', 'bonus', 'information']
    mode: Literal['visual', 'hybrid', 'code'] = 'visual'
    
    # Content
    statement: str
    setup_code: Optional[str] = None  # Python code for variable generation
    
    # Type-specific fields
    choices: Optional[List[Choice]] = None  # for multiple_choice
    questions: Optional[List[Question]] = None  # for work problems
    extras: Optional[List[str]] = None  # additional info
    
    # Metadata
    tags: List[str] = Field(default_factory=list)
    difficulty: Optional[str] = None
    topic: Optional[str] = None


class ProblemCreate(ProblemBase):
    pass


class ProblemUpdate(ProblemBase):
    pass


class Problem(ProblemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    usage_count: int = 0
    
    class Config:
        from_attributes = True


class CodeExecutionRequest(BaseModel):
    code: str
    timeout: int = 5  # seconds


class CodeExecutionResponse(BaseModel):
    success: bool
    namespace: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    figures: List[str] = Field(default_factory=list)  # base64 encoded images


class PreviewRequest(BaseModel):
    problem: ProblemCreate
    seed: Optional[int] = None  # for reproducible random values


class PreviewResponse(BaseModel):
    html: str
    namespace: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
