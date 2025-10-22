from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    pool_pre_ping=True,
    echo=settings.LOG_LEVEL == "DEBUG"
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def init_db():
    """Initialize database - create all tables."""
    from .models import Base
    Base.metadata.create_all(bind=engine)

