from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from ...domain.entities.project import Project
from ...domain.exceptions.domain_exceptions import ProjectNotFoundError
from ..ports.repositories import ProjectRepository, TaskRepository
from ..ports.event_bus import EventBus


class ProjectService:
    """Application service for project-related use cases."""
    
    def __init__(
        self,
        project_repository: ProjectRepository,
        task_repository: TaskRepository,
        event_bus: EventBus
    ):
        self.project_repo = project_repository
        self.task_repo = task_repository
        self.event_bus = event_bus
    
    def create_project(self, title: str, deadline: datetime) -> Project:
        """Use Case: Create a new project."""
        project = Project(title=title, deadline=deadline)
        
        # Publish events BEFORE saving (since save returns a new entity without events)
        self._publish_events(project)
        
        saved_project = self.project_repo.save(project)
        return saved_project
    
    def get_project(self, project_id: UUID) -> Project:
        """Use Case: Retrieve a project by ID."""
        project = self.project_repo.find_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project {project_id} not found")
        return project
    
    def get_all_projects(self) -> List[Project]:
        """Use Case: Retrieve all projects."""
        return self.project_repo.find_all()
    
    def update_project(
        self,
        project_id: UUID,
        title: Optional[str] = None,
        deadline: Optional[datetime] = None
    ) -> Project:
        """Use Case: Update project details."""
        project = self.get_project(project_id)
        
        if title is not None:
            project.title = title
        
        if deadline is not None:
            project.update_deadline(deadline)
        
        project.updated_at = datetime.now(timezone.utc)
        
        # Publish events BEFORE saving (since save returns a new entity without events)
        self._publish_events(project)
        
        updated_project = self.project_repo.save(project)
        
        return updated_project
    
    def delete_project(self, project_id: UUID) -> bool:
        """Use Case: Delete a project."""
        project = self.get_project(project_id)
        
        tasks = self.task_repo.find_by_project_id(project_id)
        for task in tasks:
            task.unlink_from_project()
            self.task_repo.save(task)
        
        return self.project_repo.delete(project_id)
    
    def link_task(self, project_id: UUID, task_id: UUID) -> None:
        """Use Case: Link a task to a project."""
        project = self.get_project(project_id)
        task = self.task_repo.find_by_id(task_id)
        
        if not task:
            from ...domain.exceptions.domain_exceptions import TaskNotFoundError
            raise TaskNotFoundError(f"Task {task_id} not found")
        
        task.link_to_project(project.id, project.deadline)
        self.task_repo.save(task)
    
    def unlink_task(self, project_id: UUID, task_id: UUID) -> None:
        """Use Case: Unlink a task from a project."""
        project = self.get_project(project_id)
        task = self.task_repo.find_by_id(task_id)
        
        if not task:
            from ...domain.exceptions.domain_exceptions import TaskNotFoundError
            raise TaskNotFoundError(f"Task {task_id} not found")
        
        task.unlink_from_project()
        self.task_repo.save(task)
    
    def _publish_events(self, entity) -> None:
        """Helper: Publish all domain events from an entity."""
        events = entity.collect_events()
        for event in events:
            self.event_bus.publish(event)

