"""
Database setup and operations
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

# Database setup
DATABASE_URL = "sqlite:///./database/problems.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ProblemDB(Base):
    """Database model for problems"""
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    mode = Column(String, default='visual')
    
    # Content
    statement = Column(Text, nullable=False)
    setup_code = Column(Text, nullable=True)
    
    # Type-specific fields (stored as JSON)
    choices = Column(JSON, nullable=True)
    questions = Column(JSON, nullable=True)
    extras = Column(JSON, nullable=True)
    
    # Metadata
    tags = Column(JSON, default=list)
    difficulty = Column(String, nullable=True)
    topic = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usage_count = Column(Integer, default=0)


def init_db():
    """Initialize the database"""
    Base.metadata.create_all(bind=engine)
    
    # Add some sample data if database is empty
    db = SessionLocal()
    try:
        if db.query(ProblemDB).count() == 0:
            sample_problems = [
                ProblemDB(
                    type='multiple_choice',
                    mode='visual',
                    statement='What is the acceleration due to gravity on Earth?',
                    choices=json.dumps([
                        {'statement': '9.8 m/s²', 'correct': True},
                        {'statement': '10 m/s²', 'correct': False},
                        {'statement': '9.81 m/s', 'correct': False},
                        {'statement': '98 m/s²', 'correct': False}
                    ]),
                    tags=json.dumps(['physics', 'gravity', 'kinematics']),
                    difficulty='easy',
                    topic='Kinematics'
                ),
                ProblemDB(
                    type='work',
                    mode='hybrid',
                    statement='A box of mass {mass} is pushed against a spring with spring constant {spring_k} until compressed by {compression}.',
                    setup_code='''import numpy as np
from quizfusion.stuff import Value

# Random parameters
mass = Value(np.random.uniform(3, 8), 'kg')
spring_k = Value(np.random.uniform(200, 500), 'N/m')
compression = Value(0.2, 'm')

# Calculate answer
max_speed = compression * np.sqrt(spring_k / mass)
energy = 0.5 * spring_k * compression**2
''',
                    questions=json.dumps([
                        {
                            'statement': 'What is the maximum speed of the box?',
                            'space': 10,
                            'points': 4,
                            'answer_code': 'max_speed'
                        },
                        {
                            'statement': 'How much energy is stored in the spring?',
                            'space': 10,
                            'points': 3,
                            'answer_code': 'energy'
                        }
                    ]),
                    tags=json.dumps(['physics', 'energy', 'springs']),
                    difficulty='medium',
                    topic='Energy Conservation'
                ),
                ProblemDB(
                    type='multiple_choice',
                    mode='hybrid',
                    statement='A projectile is launched at {angle} with velocity {velocity}. Which statement is correct?',
                    setup_code='''import numpy as np
from quizfusion.stuff import Value

angle = Value(np.random.uniform(30, 60), 'degree')
velocity = Value(np.random.uniform(20, 40), 'm/s')
''',
                    choices=json.dumps([
                        {'statement': 'The horizontal velocity changes during flight', 'correct': False},
                        {'statement': 'The vertical velocity remains constant', 'correct': False},
                        {'statement': 'The horizontal velocity remains constant', 'correct': True},
                        {'statement': 'Both velocities remain constant', 'correct': False}
                    ]),
                    tags=json.dumps(['physics', 'projectile', 'kinematics']),
                    difficulty='medium',
                    topic='Projectile Motion'
                )
            ]
            
            for problem in sample_problems:
                db.add(problem)
            
            db.commit()
    finally:
        db.close()


def get_db():
    """Dependency for getting database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
