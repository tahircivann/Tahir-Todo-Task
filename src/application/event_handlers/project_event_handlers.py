import logging
from ...domain.events.project_events import ProjectDeadlineChangedEvent
from ...domain.exceptions.domain_exceptions import InvalidDeadlineError
from ..ports.repositories import TaskRepository, ProjectRepository

logger = logging.getLogger(__name__)


class ProjectDeadlineChangedHandler:
    """Handles ProjectDeadlineChangedEvent."""
    
    def __init__(
        self,
        task_repo: TaskRepository,
        project_repo: ProjectRepository
    ):
        self.task_repo = task_repo
        self.project_repo = project_repo
    
    def handle(self, event: ProjectDeadlineChangedEvent) -> None:
        """Process project deadline change."""
        logger.info(
            f"📅 Project {event.project_id} deadline changed: "
            f"{event.old_deadline} → {event.new_deadline}"
        )
        
        if event.new_deadline >= event.old_deadline:
            return
        
        tasks = self.task_repo.find_by_project_id(event.project_id)
        
        adjusted_count = 0
        for task in tasks:
            if task.deadline > event.new_deadline:
                logger.warning(
                    f"⚠️  Task {task.id} deadline {task.deadline} exceeds "
                    f"new project deadline {event.new_deadline}. Adjusting..."
                )
                
                try:
                    task.update_deadline(
                        new_deadline=event.new_deadline,
                        project_deadline=event.new_deadline
                    )
                    self.task_repo.save(task)
                    adjusted_count += 1
                    
                    logger.info(f"✅ Adjusted task {task.id} deadline to {event.new_deadline}")
                    
                except InvalidDeadlineError as e:
                    logger.error(f"Failed to adjust task {task.id}: {e}")
        
        if adjusted_count > 0:
            logger.info(
                f"📝 Adjusted {adjusted_count} task deadline(s) for project {event.project_id}"
            )

