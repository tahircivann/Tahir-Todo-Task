from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from ..events.task_events import TaskCompletedEvent, TaskCreatedEvent, TaskDeadlineChangedEvent
from ..exceptions.domain_exceptions import InvalidDeadlineError


class Task:
    """Task entity - represents a unit of work."""
    
    def __init__(
        self,
        title: str,
        deadline: datetime,
        id: Optional[UUID] = None,
        description: Optional[str] = None,
        completed: bool = False,
        project_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id or uuid4()
        self.title = title
        self.description = description
        self.deadline = deadline
        self.completed = completed
        self.project_id = project_id
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)
        self._events: list = []
        
    def mark_completed(self) -> None:
        """Mark task as completed and emit domain event."""
        if not self.completed:
            self.completed = True
            self.updated_at = datetime.now(timezone.utc)
            self._add_event(TaskCompletedEvent(
                task_id=self.id,
                project_id=self.project_id,
                completed_at=self.updated_at
            ))
    
    def reopen(self) -> None:
        """Reopen a completed task."""
        if self.completed:
            self.completed = False
            self.updated_at = datetime.now(timezone.utc)
    
    def update_deadline(self, new_deadline: datetime, project_deadline: Optional[datetime] = None) -> None:
        """Update task deadline with validation."""
        if project_deadline and new_deadline > project_deadline:
            raise InvalidDeadlineError(
                f"Task deadline {new_deadline} cannot be later than project deadline {project_deadline}"
            )
        
        old_deadline = self.deadline
        self.deadline = new_deadline
        self.updated_at = datetime.utcnow()
        
        self._add_event(TaskDeadlineChangedEvent(
            task_id=self.id,
            old_deadline=old_deadline,
            new_deadline=new_deadline
        ))
    
    def link_to_project(self, project_id: UUID, project_deadline: datetime) -> None:
        """Link task to a project."""
        if self.deadline > project_deadline:
            raise InvalidDeadlineError(
                f"Cannot link task: task deadline {self.deadline} is later than project deadline {project_deadline}"
            )
        
        self.project_id = project_id
        self.updated_at = datetime.utcnow()
    
    def unlink_from_project(self) -> None:
        """Remove task from project."""
        self.project_id = None
        self.updated_at = datetime.utcnow()
    
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        return not self.completed and self.deadline < datetime.utcnow()
    
    def is_deadline_approaching(self, hours: int = 24) -> bool:
        """Check if deadline is approaching within specified hours."""
        if self.completed:
            return False
        
        time_until_deadline = (self.deadline - datetime.utcnow()).total_seconds() / 3600
        return 0 < time_until_deadline <= hours
    
    def _add_event(self, event) -> None:
        """Add domain event to internal queue."""
        self._events.append(event)
    
    def collect_events(self) -> list:
        """Collect and clear domain events."""
        events = self._events.copy()
        self._events.clear()
        return events
    
    def __repr__(self) -> str:
        return f"Task(id={self.id}, title='{self.title}', completed={self.completed})"
