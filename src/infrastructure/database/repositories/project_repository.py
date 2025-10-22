from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import timezone

from ....application.ports.repositories import ProjectRepository
from ....domain.entities.project import Project
from ..models import ProjectModel


class SQLAlchemyProjectRepository(ProjectRepository):
    """Adapter: Implements ProjectRepository port using SQLAlchemy."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def save(self, project: Project) -> Project:
        """Save or update a project."""
        project_model = self.session.query(ProjectModel)\
            .filter_by(id=project.id).first()
        
        if project_model:
            project_model.title = project.title
            project_model.deadline = project.deadline
            project_model.completed = project.completed
            project_model.updated_at = project.updated_at
        else:
            project_model = ProjectModel(
                id=project.id,
                title=project.title,
                deadline=project.deadline,
                completed=project.completed,
                created_at=project.created_at,
                updated_at=project.updated_at
            )
            self.session.add(project_model)
        
        self.session.commit()
        return self._to_domain(project_model)
    
    def find_by_id(self, project_id: UUID) -> Optional[Project]:
        """Retrieve a project by its ID."""
        project_model = self.session.query(ProjectModel)\
            .filter_by(id=project_id).first()
        return self._to_domain(project_model) if project_model else None
    
    def find_all(self) -> List[Project]:
        """Retrieve all projects."""
        project_models = self.session.query(ProjectModel)\
            .order_by(ProjectModel.created_at.desc())\
            .all()
        return [self._to_domain(pm) for pm in project_models]
    
    def delete(self, project_id: UUID) -> bool:
        """Delete a project by ID."""
        project_model = self.session.query(ProjectModel)\
            .filter_by(id=project_id).first()
        if project_model:
            self.session.delete(project_model)
            self.session.commit()
            return True
        return False
    
    def _to_domain(self, model: ProjectModel) -> Project:
        """Convert database model to domain entity."""
        # Ensure timezone-aware datetimes
        deadline = model.deadline
        if deadline.tzinfo is None:
            deadline = deadline.replace(tzinfo=timezone.utc)
        
        created_at = model.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
            
        updated_at = model.updated_at
        if updated_at.tzinfo is None:
            updated_at = updated_at.replace(tzinfo=timezone.utc)
        
        return Project(
            id=model.id,
            title=model.title,
            deadline=deadline,
            completed=model.completed,
            created_at=created_at,
            updated_at=updated_at
        )
