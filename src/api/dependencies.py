from functools import lru_cache
from fastapi import Depends
from sqlalchemy.orm import Session

from ..infrastructure.database.session import SessionLocal
from ..infrastructure.database.repositories.task_repository import SQLAlchemyTaskRepository
from ..infrastructure.database.repositories.project_repository import SQLAlchemyProjectRepository
from ..infrastructure.event_bus.in_memory_event_bus import InMemoryEventBus
from ..application.services.task_service import TaskService
from ..application.services.project_service import ProjectService


def get_db():
    """Dependency: Database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache()
def get_event_bus() -> InMemoryEventBus:
    """Dependency: Event bus singleton."""
    return InMemoryEventBus()


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """Dependency: Task service with all dependencies injected."""
    task_repo = SQLAlchemyTaskRepository(db)
    project_repo = SQLAlchemyProjectRepository(db)
    event_bus = get_event_bus()
    return TaskService(task_repo, project_repo, event_bus)


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    """Dependency: Project service with all dependencies injected."""
    project_repo = SQLAlchemyProjectRepository(db)
    task_repo = SQLAlchemyTaskRepository(db)
    event_bus = get_event_bus()
    return ProjectService(project_repo, task_repo, event_bus)