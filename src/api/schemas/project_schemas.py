from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID


class ProjectBase(BaseModel):
    """Base schema for project data."""
    title: str = Field(..., min_length=1, max_length=200)
    deadline: datetime


class ProjectCreate(ProjectBase):
    """Schema for creating a project."""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    deadline: Optional[datetime] = None


class ProjectResponse(ProjectBase):
    """Schema for project responses."""
    id: UUID
    completed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

