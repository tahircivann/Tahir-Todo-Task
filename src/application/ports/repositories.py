from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ...domain.entities.task import Task
from ...domain.entities.project import Project


class TaskRepository(ABC):
    """Port (interface) for Task persistence."""
    
    @abstractmethod
    def save(self, task: Task) -> Task:
        """Save or update a task."""
        pass
    
    @abstractmethod
    def find_by_id(self, task_id: UUID) -> Optional[Task]:
        """Find a task by ID."""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Task]:
        """Retrieve all tasks."""
        pass
    
    @abstractmethod
    def find_by_project_id(self, project_id: UUID) -> List[Task]:
        """Find all tasks belonging to a project."""
        pass
    
    @abstractmethod
    def find_completed(self) -> List[Task]:
        """Find all completed tasks."""
        pass
    
    @abstractmethod
    def find_overdue(self) -> List[Task]:
        """Find all overdue tasks."""
        pass
    
    @abstractmethod
    def delete(self, task_id: UUID) -> bool:
        """Delete a task by ID."""
        pass


class ProjectRepository(ABC):
    """Port (interface) for Project persistence."""
    
    @abstractmethod
    def save(self, project: Project) -> Project:
        """Save or update a project."""
        pass
    
    @abstractmethod
    def find_by_id(self, project_id: UUID) -> Optional[Project]:
        """Find a project by ID."""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Project]:
        """Retrieve all projects."""
        pass
    
    @abstractmethod
    def delete(self, project_id: UUID) -> bool:
        """Delete a project by ID."""
        pass

