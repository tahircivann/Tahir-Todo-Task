from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from uuid import UUID

from ..schemas.task_schemas import TaskCreate, TaskResponse, TaskUpdate
from ..dependencies import get_task_service
from ...application.services.task_service import TaskService
from ...domain.exceptions.domain_exceptions import (
    TaskNotFoundError,
    InvalidDeadlineError,
    ProjectNotFoundError
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task"
)
def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service)
):
    """Create a new task."""
    try:
        task = service.create_task(
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline,
            project_id=task_data.project_id
        )
        return task
    except InvalidDeadlineError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/", response_model=List[TaskResponse], summary="List all tasks")
def list_tasks(
    completed: Optional[bool] = Query(None),
    overdue: Optional[bool] = Query(None),
    project_id: Optional[UUID] = Query(None),
    service: TaskService = Depends(get_task_service)
):
    """Retrieve a list of tasks with optional filters."""
    if completed is not None:
        if completed:
            return service.get_completed_tasks()
        else:
            all_tasks = service.get_all_tasks()
            return [t for t in all_tasks if not t.completed]
    
    if overdue:
        return service.get_overdue_tasks()
    
    if project_id:
        try:
            return service.get_tasks_by_project(project_id)
        except ProjectNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    return service.get_all_tasks()


@router.get("/{task_id}", response_model=TaskResponse, summary="Get a task")
def get_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service)
):
    """Retrieve a single task by its ID."""
    try:
        return service.get_task(task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{task_id}", response_model=TaskResponse, summary="Update a task")
def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    """Update an existing task."""
    try:
        return service.update_task(
            task_id=task_id,
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline
        )
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidDeadlineError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task"
)
def delete_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service)
):
    """Delete a task."""
    try:
        service.delete_task(task_id)
        return None
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch(
    "/{task_id}/complete",
    response_model=TaskResponse,
    summary="Mark task as completed"
)
def complete_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service)
):
    """Mark a task as completed."""
    try:
        return service.complete_task(task_id, auto_complete_project=True)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

