from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID


class TaskBase(BaseModel):
    """Base schema for task data."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    deadline: datetime


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    project_id: Optional[UUID] = None


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    deadline: Optional[datetime] = None


class TaskResponse(TaskBase):
    """Schema for task responses."""
    id: UUID
    completed: bool
    project_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
