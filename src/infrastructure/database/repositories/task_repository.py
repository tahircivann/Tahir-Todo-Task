from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from ....application.ports.repositories import TaskRepository
from ....domain.entities.task import Task
from ..models import TaskModel


class SQLAlchemyTaskRepository(TaskRepository):
    """Adapter: Implements TaskRepository port using SQLAlchemy."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def save(self, task: Task) -> Task:
        """Save or update a task."""
        task_model = self.session.query(TaskModel).filter_by(id=task.id).first()
        
        if task_model:
            task_model.title = task.title
            task_model.description = task.description
            task_model.deadline = task.deadline
            task_model.completed = task.completed
            task_model.project_id = task.project_id
            task_model.updated_at = task.updated_at
        else:
            task_model = TaskModel(
                id=task.id,
                title=task.title,
                description=task.description,
                deadline=task.deadline,
                completed=task.completed,
                project_id=task.project_id,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            self.session.add(task_model)
        
        self.session.commit()
        return self._to_domain(task_model)
    
    def find_by_id(self, task_id: UUID) -> Optional[Task]:
        """Retrieve a task by its ID."""
        task_model = self.session.query(TaskModel).filter_by(id=task_id).first()
        return self._to_domain(task_model) if task_model else None
    
    def find_all(self) -> List[Task]:
        """Retrieve all tasks."""
        task_models = self.session.query(TaskModel).all()
        return [self._to_domain(tm) for tm in task_models]
    
    def find_by_project_id(self, project_id: UUID) -> List[Task]:
        """Find all tasks belonging to a specific project."""
        task_models = self.session.query(TaskModel)\
            .filter_by(project_id=project_id)\
            .order_by(TaskModel.created_at)\
            .all()
        return [self._to_domain(tm) for tm in task_models]
    
    def find_completed(self) -> List[Task]:
        """Find all completed tasks."""
        task_models = self.session.query(TaskModel)\
            .filter_by(completed=True)\
            .order_by(TaskModel.updated_at.desc())\
            .all()
        return [self._to_domain(tm) for tm in task_models]
    
    def find_overdue(self) -> List[Task]:
        """Find all overdue tasks."""
        now = datetime.utcnow()
        task_models = self.session.query(TaskModel)\
            .filter(
                TaskModel.completed == False,
                TaskModel.deadline < now
            )\
            .order_by(TaskModel.deadline)\
            .all()
        return [self._to_domain(tm) for tm in task_models]
    
    def delete(self, task_id: UUID) -> bool:
        """Delete a task by ID."""
        task_model = self.session.query(TaskModel).filter_by(id=task_id).first()
        if task_model:
            self.session.delete(task_model)
            self.session.commit()
            return True
        return False
    
    def _to_domain(self, model: TaskModel) -> Task:
        """Convert database model to domain entity."""
        # Ensure timezone-aware datetimes
        deadline = model.deadline
        if deadline.tzinfo is None:
            deadline = deadline.replace(tzinfo=timezone.utc)
        
        created_at = model.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
            
        updated_at = model.updated_at
        if updated_at.tzinfo is None:
            updated_at = updated_at.replace(tzinfo=timezone.utc)
        
        return Task(
            id=model.id,
            title=model.title,
            description=model.description,
            deadline=deadline,
            completed=model.completed,
            project_id=model.project_id,
            created_at=created_at,
            updated_at=updated_at
        )
