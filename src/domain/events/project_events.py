from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ..entities.base import DomainEvent


@dataclass
class ProjectCreatedEvent(DomainEvent):
    """Emitted when a new project is created."""
    project_id: UUID
    title: str
    deadline: datetime
    
    def __post_init__(self):
        super().__post_init__()


@dataclass
class ProjectCompletedEvent(DomainEvent):
    """Emitted when a project is marked as completed."""
    project_id: UUID
    completed_at: datetime
    
    def __post_init__(self):
        super().__post_init__()


@dataclass
class ProjectReopenedEvent(DomainEvent):
    """Emitted when a completed project is reopened."""
    project_id: UUID
    reopened_at: datetime
    
    def __post_init__(self):
        super().__post_init__()


@dataclass
class ProjectDeadlineChangedEvent(DomainEvent):
    """Emitted when a project's deadline is changed."""
    project_id: UUID
    old_deadline: datetime
    new_deadline: datetime
    
    def __post_init__(self):
        super().__post_init__()