import pytest
from datetime import datetime, timedelta
from uuid import UUID

from src.domain.entities.task import Task
from src.domain.exceptions.domain_exceptions import InvalidDeadlineError
from src.domain.events.task_events import TaskCompletedEvent


class TestTaskEntity:
    """Test suite for Task entity business logic."""
    
    def test_task_creation(self):
        """Test creating a task with valid data."""
        deadline = datetime.utcnow() + timedelta(days=5)
        task = Task(
            title="Write tests",
            description="Unit tests for task entity",
            deadline=deadline
        )
        
        assert task.title == "Write tests"
        assert task.description == "Unit tests for task entity"
        assert task.deadline == deadline
        assert task.completed is False
        assert isinstance(task.id, UUID)
        assert task.project_id is None
    
    def test_mark_completed_emits_event(self):
        """Test that completing a task emits TaskCompletedEvent."""
        task = Task(
            title="Test Task",
            deadline=datetime.utcnow() + timedelta(days=5)
        )
        
        task.mark_completed()
        
        assert task.completed is True
        
        events = task.collect_events()
        assert len(events) == 1
        assert isinstance(events[0], TaskCompletedEvent)
        assert events[0].task_id == task.id
    
    def test_update_deadline_within_project_constraint(self):
        """Test updating deadline when it respects project constraint."""
        task = Task(
            title="Task",
            deadline=datetime.utcnow() + timedelta(days=5)
        )
        
        new_deadline = datetime.utcnow() + timedelta(days=3)
        project_deadline = datetime.utcnow() + timedelta(days=10)
        
        task.update_deadline(new_deadline, project_deadline)
        
        assert task.deadline == new_deadline
    
    def test_update_deadline_violates_project_constraint(self):
        """Test that updating deadline to exceed project deadline raises error."""
        task = Task(
            title="Task",
            deadline=datetime.utcnow() + timedelta(days=5)
        )
        
        new_deadline = datetime.utcnow() + timedelta(days=15)
        project_deadline = datetime.utcnow() + timedelta(days=10)
        
        with pytest.raises(InvalidDeadlineError) as exc_info:
            task.update_deadline(new_deadline, project_deadline)
        
        assert "cannot be later than project deadline" in str(exc_info.value)
    
    def test_link_to_project_with_valid_deadline(self):
        """Test linking task to project when deadline is valid."""
        task = Task(
            title="Task",
            deadline=datetime.utcnow() + timedelta(days=5)
        )
        
        from uuid import UUID
        project_id = UUID('12345678-1234-5678-1234-567812345678')
        project_deadline = datetime.utcnow() + timedelta(days=10)
        
        task.link_to_project(project_id, project_deadline)
        
        assert task.project_id == project_id
    
    def test_link_to_project_with_invalid_deadline(self):
        """Test that linking fails when task deadline exceeds project deadline."""
        task = Task(
            title="Task",
            deadline=datetime.utcnow() + timedelta(days=15)
        )
        
        from uuid import UUID
        project_id = UUID('12345678-1234-5678-1234-567812345678')
        project_deadline = datetime.utcnow() + timedelta(days=10)
        
        with pytest.raises(InvalidDeadlineError):
            task.link_to_project(project_id, project_deadline)
        
        assert task.project_id is None
    
    def test_is_overdue(self):
        """Test overdue detection."""
        overdue_task = Task(
            title="Overdue",
            deadline=datetime.utcnow() - timedelta(days=1)
        )
        assert overdue_task.is_overdue() is True
        
        future_task = Task(
            title="Future",
            deadline=datetime.utcnow() + timedelta(days=1)
        )
        assert future_task.is_overdue() is False
        
        overdue_task.mark_completed()
        assert overdue_task.is_overdue() is False
    
    def test_is_deadline_approaching(self):
        """Test deadline approaching detection."""
        approaching_task = Task(
            title="Soon",
            deadline=datetime.utcnow() + timedelta(hours=12)
        )
        assert approaching_task.is_deadline_approaching(hours=24) is True
        
        distant_task = Task(
            title="Later",
            deadline=datetime.utcnow() + timedelta(hours=48)
        )
        assert distant_task.is_deadline_approaching(hours=24) is False
        
        approaching_task.mark_completed()
        assert approaching_task.is_deadline_approaching(hours=24) is False
