from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from ..schemas.project_schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from ..schemas.task_schemas import TaskResponse
from ..dependencies import get_project_service, get_task_service
from ...application.services.project_service import ProjectService
from ...application.services.task_service import TaskService
from ...domain.exceptions.domain_exceptions import (
    ProjectNotFoundError,
    TaskNotFoundError,
    InvalidDeadlineError
)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project"
)
def create_project(
    project_data: ProjectCreate,
    service: ProjectService = Depends(get_project_service)
):
    """Create a new project."""
    project = service.create_project(
        title=project_data.title,
        deadline=project_data.deadline
    )
    return project


@router.get("/", response_model=List[ProjectResponse], summary="List all projects")
def list_projects(
    service: ProjectService = Depends(get_project_service)
):
    """Retrieve a list of all projects."""
    return service.get_all_projects()


@router.get("/{project_id}", response_model=ProjectResponse, summary="Get a project")
def get_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service)
):
    """Retrieve a single project by its ID."""
    try:
        return service.get_project(project_id)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{project_id}", response_model=ProjectResponse, summary="Update a project")
def update_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    service: ProjectService = Depends(get_project_service)
):
    """Update an existing project."""
    try:
        return service.update_project(
            project_id=project_id,
            title=project_data.title,
            deadline=project_data.deadline
        )
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project"
)
def delete_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service)
):
    """Delete a project."""
    try:
        service.delete_project(project_id)
        return None
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    "/{project_id}/tasks/{task_id}/link",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Link task to project"
)
def link_task_to_project(
    project_id: UUID,
    task_id: UUID,
    service: ProjectService = Depends(get_project_service)
):
    """Link a task to a project."""
    try:
        service.link_task(project_id, task_id)
        return None
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidDeadlineError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{project_id}/tasks/{task_id}/unlink",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Unlink task from project"
)
def unlink_task_from_project(
    project_id: UUID,
    task_id: UUID,
    service: ProjectService = Depends(get_project_service)
):
    """Unlink a task from a project."""
    try:
        service.unlink_task(project_id, task_id)
        return None
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/{project_id}/tasks",
    response_model=List[TaskResponse],
    summary="Get project tasks"
)
def get_project_tasks(
    project_id: UUID,
    task_service: TaskService = Depends(get_task_service)
):
    """Retrieve all tasks for a specific project."""
    try:
        return task_service.get_tasks_by_project(project_id)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))