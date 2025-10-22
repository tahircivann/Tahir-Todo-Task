from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator, CHAR
import uuid
from datetime import datetime, timezone

Base = declarative_base()


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses CHAR(36), storing as stringified hex values.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            from sqlalchemy.dialects.postgresql import UUID
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value)
            return value


class TaskModel(Base):
    """SQLAlchemy ORM model for Task."""
    __tablename__ = "tasks"
    
    id = Column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    
    title = Column(String(200), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    deadline = Column(DateTime, nullable=False, index=True)
    completed = Column(Boolean, default=False, nullable=False, index=True)
    
    project_id = Column(
        GUID(),
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    __table_args__ = (
        Index('ix_tasks_project_completed', 'project_id', 'completed'),
        Index('ix_tasks_completed_deadline', 'completed', 'deadline'),
    )
    
    def __repr__(self):
        return f"<TaskModel(id={self.id}, title='{self.title}', completed={self.completed})>"


class ProjectModel(Base):
    """SQLAlchemy ORM model for Project."""
    __tablename__ = "projects"
    
    id = Column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    
    title = Column(String(200), nullable=False, index=True)
    deadline = Column(DateTime, nullable=False, index=True)
    completed = Column(Boolean, default=False, nullable=False, index=True)
    
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<ProjectModel(id={self.id}, title='{self.title}', completed={self.completed})>"

