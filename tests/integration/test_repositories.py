import pytest
from datetime import datetime, timedelta

from src.domain.entities.task import Task
from src.domain.entities.project import Project


class TestTaskRepository:
    """Test suite for TaskRepository implementation."""
    
    def test_save_and_find_task(self, task_repository):
        """Test saving and retrieving a task."""
        task = Task(
            title="Integration Test Task",
            description="Testing repository",
            deadline=datetime.utcnow() + timedelta(days=7)
        )
        
        saved_task = task_repository.save(task)
        
        found_task = task_repository.find_by_id(saved_task.id)
        
        assert found_task is not None
        assert found_task.id == task.id
        assert found_task.title == "Integration Test Task"
        assert found_task.description == "Testing repository"
    
    def test_update_task(self, task_repository):
        """Test updating an existing task."""
        task = Task(
            title="Original Title",
            deadline=datetime.utcnow() + timedelta(days=7)
        )
        
        saved_task = task_repository.save(task)
        
        saved_task.title = "Updated Title"
        saved_task.mark_completed()
        
        updated_task = task_repository.save(saved_task)
        
        assert updated_task.title == "Updated Title"
        assert updated_task.completed is True
    
    def test_find_all_tasks(self, task_repository):
        """Test retrieving all tasks."""
        for i in range(3):
            task = Task(
                title=f"Task {i}",
                deadline=datetime.utcnow() + timedelta(days=i+1)
            )
            task_repository.save(task)
        
        all_tasks = task_repository.find_all()
        assert len(all_tasks) == 3
    
    def test_find_completed_tasks(self, task_repository):
        """Test filtering completed tasks."""
        completed_task = Task(title="Done", deadline=datetime.utcnow())
        completed_task.mark_completed()
        task_repository.save(completed_task)
        
        incomplete_task = Task(title="Todo", deadline=datetime.utcnow())
        task_repository.save(incomplete_task)
        
        completed = task_repository.find_completed()
        assert len(completed) == 1
        assert completed[0].title == "Done"
    
    def test_delete_task(self, task_repository):
        """Test deleting a task."""
        task = Task(
            title="To Delete",
            deadline=datetime.utcnow() + timedelta(days=1)
        )
        saved_task = task_repository.save(task)
        
        result = task_repository.delete(saved_task.id)
        assert result is True
        
        found = task_repository.find_by_id(saved_task.id)
        assert found is None


class TestProjectRepository:
    """Test suite for ProjectRepository implementation."""
    
    def test_save_and_find_project(self, project_repository):
        """Test saving and retrieving a project."""
        project = Project(
            title="Test Project",
            deadline=datetime.utcnow() + timedelta(days=30)
        )
        
        saved_project = project_repository.save(project)
        found_project = project_repository.find_by_id(saved_project.id)
        
        assert found_project is not None
        assert found_project.title == "Test Project"
    
    def test_find_all_projects(self, project_repository):
        """Test retrieving all projects."""
        for i in range(2):
            project = Project(
                title=f"Project {i}",
                deadline=datetime.utcnow() + timedelta(days=30)
            )
            project_repository.save(project)
        
        all_projects = project_repository.find_all()
        assert len(all_projects) == 2