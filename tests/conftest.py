import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4

from src.infrastructure.database.models import Base
from src.infrastructure.database.repositories.task_repository import SQLAlchemyTaskRepository
from src.infrastructure.database.repositories.project_repository import SQLAlchemyProjectRepository
from src.infrastructure.event_bus.in_memory_event_bus import InMemoryEventBus
from src.domain.entities.task import Task
from src.domain.entities.project import Project


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def task_repository(db_session):
    """Fixture for task repository."""
    return SQLAlchemyTaskRepository(db_session)


@pytest.fixture
def project_repository(db_session):
    """Fixture for project repository."""
    return SQLAlchemyProjectRepository(db_session)


@pytest.fixture
def event_bus():
    """Fixture for event bus."""
    return InMemoryEventBus()


@pytest.fixture
def sample_task():
    """Fixture for a sample task entity."""
    return Task(
        title="Test Task",
        description="Test description",
        deadline=datetime.utcnow() + timedelta(days=7)
    )


@pytest.fixture
def sample_project():
    """Fixture for a sample project entity."""
    return Project(
        title="Test Project",
        deadline=datetime.utcnow() + timedelta(days=30)
    )
