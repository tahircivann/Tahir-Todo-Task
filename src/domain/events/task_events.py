from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from ..entities.base import DomainEvent


@dataclass
class TaskCreatedEvent(DomainEvent):
    """Emitted when a new task is created."""
    task_id: UUID
    title: str
    deadline: datetime
    
    def __post_init__(self):
        super().__post_init__()


@dataclass
class TaskCompletedEvent(DomainEvent):
    """Emitted when a task is marked as completed."""
    task_id: UUID
    project_id: Optional[UUID]
    completed_at: datetime
    
    def __post_init__(self):
        super().__post_init__()


@dataclass
class TaskReopenedEvent(DomainEvent):
    """Emitted when a completed task is reopened."""
    task_id: UUID
    project_id: Optional[UUID]
    
    def __post_init__(self):
        super().__post_init__()


@dataclass
class TaskDeadlineChangedEvent(DomainEvent):
    """Emitted when a task's deadline is changed."""
    task_id: UUID
    old_deadline: datetime
    new_deadline: datetime
    
    def __post_init__(self):
        super().__post_init__()