from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from ..events.project_events import (
    ProjectCompletedEvent,
    ProjectDeadlineChangedEvent,
    ProjectReopenedEvent
)
from ..exceptions.domain_exceptions import ProjectCompletionError


class Project:
    """Project entity - represents a container for tasks."""
    
    def __init__(
        self,
        title: str,
        deadline: datetime,
        id: Optional[UUID] = None,
        completed: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id or uuid4()
        self.title = title
        self.deadline = deadline
        self.completed = completed
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)
        self._events: list = []
    
    def mark_completed(self, all_tasks_completed: bool) -> None:
        """Mark project as completed."""
        if not all_tasks_completed:
            raise ProjectCompletionError(
                f"Cannot complete project {self.id}: not all tasks are completed"
            )
        
        if not self.completed:
            self.completed = True
            self.updated_at = datetime.now(timezone.utc)
            self._add_event(ProjectCompletedEvent(
                project_id=self.id,
                completed_at=self.updated_at
            ))
    
    def reopen(self) -> None:
        """Reopen a completed project."""
        if self.completed:
            self.completed = False
            self.updated_at = datetime.now(timezone.utc)
            self._add_event(ProjectReopenedEvent(
                project_id=self.id,
                reopened_at=self.updated_at
            ))
    
    def update_deadline(self, new_deadline: datetime) -> None:
        """Update project deadline."""
        old_deadline = self.deadline
        self.deadline = new_deadline
        self.updated_at = datetime.now(timezone.utc)
        
        self._add_event(ProjectDeadlineChangedEvent(
            project_id=self.id,
            old_deadline=old_deadline,
            new_deadline=new_deadline
        ))
    
    def _add_event(self, event) -> None:
        """Add domain event to internal queue."""
        self._events.append(event)
    
    def collect_events(self) -> list:
        """Collect and clear domain events."""
        events = self._events.copy()
        self._events.clear()
        return events
    
    def __repr__(self) -> str:
        return f"Project(id={self.id}, title='{self.title}', completed={self.completed})"

