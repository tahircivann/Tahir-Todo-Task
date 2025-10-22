import pytest
from datetime import datetime, timedelta

from src.domain.entities.project import Project
from src.domain.exceptions.domain_exceptions import ProjectCompletionError
from src.domain.events.project_events import ProjectCompletedEvent, ProjectDeadlineChangedEvent


class TestProjectEntity:
    """Test suite for Project entity business logic."""
    
    def test_project_creation(self):
        """Test creating a project with valid data."""
        deadline = datetime.utcnow() + timedelta(days=30)
        project = Project(
            title="Q4 Goals",
            deadline=deadline
        )
        
        assert project.title == "Q4 Goals"
        assert project.deadline == deadline
        assert project.completed is False
    
    def test_mark_completed_with_all_tasks_done(self):
        """Test completing project when all tasks are completed."""
        project = Project(
            title="Project",
            deadline=datetime.utcnow() + timedelta(days=30)
        )
        
        project.mark_completed(all_tasks_completed=True)
        
        assert project.completed is True
        
        events = project.collect_events()
        assert len(events) == 1
        assert isinstance(events[0], ProjectCompletedEvent)
    
    def test_mark_completed_with_incomplete_tasks_raises_error(self):
        """Test that completing project with incomplete tasks raises error."""
        project = Project(
            title="Project",
            deadline=datetime.utcnow() + timedelta(days=30)
        )
        
        with pytest.raises(ProjectCompletionError) as exc_info:
            project.mark_completed(all_tasks_completed=False)
        
        assert "not all tasks are completed" in str(exc_info.value)
        assert project.completed is False
    
    def test_update_deadline_emits_event(self):
        """Test that updating deadline emits event."""
        project = Project(
            title="Project",
            deadline=datetime.utcnow() + timedelta(days=30)
        )
        
        new_deadline = datetime.utcnow() + timedelta(days=15)
        project.update_deadline(new_deadline)
        
        assert project.deadline == new_deadline
        
        events = project.collect_events()
        assert len(events) == 1
        assert isinstance(events[0], ProjectDeadlineChangedEvent)
    
    def test_reopen_project(self):
        """Test reopening a completed project."""
        project = Project(
            title="Project",
            deadline=datetime.utcnow() + timedelta(days=30)
        )
        
        project.mark_completed(all_tasks_completed=True)
        assert project.completed is True
        
        project.reopen()
        assert project.completed is False

