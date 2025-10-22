import logging
from datetime import datetime, timedelta

from ...domain.events.task_events import TaskCompletedEvent, TaskReopenedEvent
from ..ports.repositories import TaskRepository, ProjectRepository

logger = logging.getLogger(__name__)


class TaskCompletedHandler:
    """Handles TaskCompletedEvent."""
    
    def __init__(
        self,
        task_repo: TaskRepository,
        project_repo: ProjectRepository,
        auto_complete_project: bool = False
    ):
        self.task_repo = task_repo
        self.project_repo = project_repo
        self.auto_complete_project = auto_complete_project
    
    def handle(self, event: TaskCompletedEvent) -> None:
        """Process task completion."""
        logger.info(f"✅ Task {event.task_id} completed at {event.completed_at}")
        
        if event.project_id and self.auto_complete_project:
            self._check_project_completion(event.project_id)
    
    def _check_project_completion(self, project_id) -> None:
        """Check if all project tasks are completed."""
        tasks = self.task_repo.find_by_project_id(project_id)
        
        if not tasks:
            return
        
        all_completed = all(task.completed for task in tasks)
        
        if all_completed:
            project = self.project_repo.find_by_id(project_id)
            if project and not project.completed:
                logger.info(f"🎉 All tasks completed! Auto-completing project {project_id}")
                try:
                    project.mark_completed(all_tasks_completed=True)
                    self.project_repo.save(project)
                except Exception as e:
                    logger.error(f"Failed to auto-complete project: {e}")


class TaskReopenedHandler:
    """Handles TaskReopenedEvent."""
    
    def __init__(self, project_repo: ProjectRepository):
        self.project_repo = project_repo
    
    def handle(self, event: TaskReopenedEvent) -> None:
        """Process task reopening."""
        logger.info(f"🔄 Task {event.task_id} reopened")
        
        if event.project_id:
            project = self.project_repo.find_by_id(event.project_id)
            if project and project.completed:
                logger.info(f"Reopening project {event.project_id} due to task reopening")
                project.reopen()
                self.project_repo.save(project)


class DeadlineApproachingHandler:
    """Periodically checks for tasks with approaching deadlines."""
    
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo
    
    def check_approaching_deadlines(self, hours: int = 24) -> None:
        """Check all tasks for approaching deadlines."""
        tasks = self.task_repo.find_all()
        
        for task in tasks:
            if task.is_deadline_approaching(hours):
                logger.warning(
                    f"⚠️  Task '{task.title}' (ID: {task.id}) deadline approaching! "
                    f"Due: {task.deadline}"
                )

