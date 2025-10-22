from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from ...domain.entities.task import Task
from ...domain.exceptions.domain_exceptions import TaskNotFoundError, ProjectNotFoundError
from ..ports.repositories import TaskRepository, ProjectRepository
from ..ports.event_bus import EventBus


class TaskService:
    """Application service for task-related use cases."""
    
    def __init__(
        self,
        task_repository: TaskRepository,
        project_repository: ProjectRepository,
        event_bus: EventBus
    ):
        self.task_repo = task_repository
        self.project_repo = project_repository
        self.event_bus = event_bus
    
    def create_task(
        self,
        title: str,
        deadline: datetime,
        description: Optional[str] = None,
        project_id: Optional[UUID] = None
    ) -> Task:
        """Use Case: Create a new task."""
        if project_id:
            project = self.project_repo.find_by_id(project_id)
            if not project:
                raise ProjectNotFoundError(f"Project {project_id} not found")
            
            if deadline > project.deadline:
                from ...domain.exceptions.domain_exceptions import InvalidDeadlineError
                raise InvalidDeadlineError(
                    f"Task deadline cannot be later than project deadline {project.deadline}"
                )
        
        task = Task(
            title=title,
            description=description,
            deadline=deadline,
            project_id=project_id
        )
        
        saved_task = self.task_repo.save(task)
        self._publish_events(saved_task)
        
        return saved_task
    
    def get_task(self, task_id: UUID) -> Task:
        """Use Case: Retrieve a task by ID."""
        task = self.task_repo.find_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task
    
    def get_all_tasks(self) -> List[Task]:
        """Use Case: Retrieve all tasks."""
        return self.task_repo.find_all()
    
    def update_task(
        self,
        task_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        deadline: Optional[datetime] = None
    ) -> Task:
        """Use Case: Update task details."""
        task = self.get_task(task_id)
        
        if title is not None:
            task.title = title
        
        if description is not None:
            task.description = description
        
        if deadline is not None:
            project_deadline = None
            if task.project_id:
                project = self.project_repo.find_by_id(task.project_id)
                if project:
                    project_deadline = project.deadline
            
            task.update_deadline(deadline, project_deadline)
        
        task.updated_at = datetime.now(timezone.utc)
        
        updated_task = self.task_repo.save(task)
        self._publish_events(updated_task)
        
        return updated_task
    
    def delete_task(self, task_id: UUID) -> bool:
        """Use Case: Delete a task."""
        task = self.get_task(task_id)
        return self.task_repo.delete(task_id)
    
    def complete_task(self, task_id: UUID, auto_complete_project: bool = False) -> Task:
        """Use Case: Mark a task as completed."""
        task = self.get_task(task_id)
        
        task.mark_completed()
        
        completed_task = self.task_repo.save(task)
        
        self._publish_events(completed_task)
        
        if auto_complete_project and task.project_id:
            self._try_auto_complete_project(task.project_id)
        
        return completed_task
    
    def get_tasks_by_project(self, project_id: UUID) -> List[Task]:
        """Use Case: Get all tasks for a project."""
        project = self.project_repo.find_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project {project_id} not found")
        
        return self.task_repo.find_by_project_id(project_id)
    
    def get_overdue_tasks(self) -> List[Task]:
        """Use Case: Get all overdue tasks."""
        return self.task_repo.find_overdue()
    
    def get_completed_tasks(self) -> List[Task]:
        """Use Case: Get all completed tasks."""
        return self.task_repo.find_completed()
    
    def _try_auto_complete_project(self, project_id: UUID) -> None:
        """Helper: Auto-complete project if all tasks are done."""
        tasks = self.task_repo.find_by_project_id(project_id)
        all_completed = all(task.completed for task in tasks)
        
        if all_completed and tasks:
            project = self.project_repo.find_by_id(project_id)
            if project and not project.completed:
                project.mark_completed(all_tasks_completed=True)
                self.project_repo.save(project)
                self._publish_events(project)
    
    def _publish_events(self, entity) -> None:
        """Helper: Publish all domain events from an entity."""
        events = entity.collect_events()
        for event in events:
            self.event_bus.publish(event)
