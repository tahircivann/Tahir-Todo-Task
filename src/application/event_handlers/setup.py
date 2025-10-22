import logging
from ..ports.event_bus import EventBus
from ..ports.repositories import TaskRepository, ProjectRepository
from ...domain.events.task_events import TaskCompletedEvent, TaskReopenedEvent
from ...domain.events.project_events import ProjectDeadlineChangedEvent
from .task_event_handlers import (
    TaskCompletedHandler,
    TaskReopenedHandler,
    DeadlineApproachingHandler
)
from .project_event_handlers import ProjectDeadlineChangedHandler

logger = logging.getLogger(__name__)


def setup_event_handlers(
    event_bus: EventBus,
    task_repo: TaskRepository,
    project_repo: ProjectRepository,
    auto_complete_project: bool = False
) -> None:
    """Register all event handlers with the event bus."""
    logger.info("🔧 Setting up event handlers...")
    
    task_completed_handler = TaskCompletedHandler(
        task_repo=task_repo,
        project_repo=project_repo,
        auto_complete_project=auto_complete_project
    )
    event_bus.subscribe(TaskCompletedEvent, task_completed_handler.handle)
    
    task_reopened_handler = TaskReopenedHandler(project_repo=project_repo)
    event_bus.subscribe(TaskReopenedEvent, task_reopened_handler.handle)
    
    deadline_changed_handler = ProjectDeadlineChangedHandler(
        task_repo=task_repo,
        project_repo=project_repo
    )
    event_bus.subscribe(ProjectDeadlineChangedEvent, deadline_changed_handler.handle)
    
    logger.info("✅ Event handlers registered successfully")