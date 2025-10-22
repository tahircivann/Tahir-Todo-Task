import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import tasks, projects
from ..infrastructure.database.models import Base
from ..infrastructure.database.session import engine, SessionLocal
from ..infrastructure.database.repositories.task_repository import SQLAlchemyTaskRepository
from ..infrastructure.database.repositories.project_repository import SQLAlchemyProjectRepository
from ..application.event_handlers.setup import setup_event_handlers
from .dependencies import get_event_bus
from ..infrastructure.config.settings import settings

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("🚀 Starting Task Management System...")
    
    logger.info("📊 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    logger.info("🔧 Registering event handlers...")
    db = SessionLocal()
    try:
        task_repo = SQLAlchemyTaskRepository(db)
        project_repo = SQLAlchemyProjectRepository(db)
        event_bus = get_event_bus()
        
        setup_event_handlers(
            event_bus=event_bus,
            task_repo=task_repo,
            project_repo=project_repo,
            auto_complete_project=settings.AUTO_COMPLETE_PROJECT
        )
    finally:
        db.close()
    
    logger.info("✅ Application started successfully!")
    
    yield
    
    logger.info("👋 Shutting down Task Management System...")


app = FastAPI(
    title="Task Management System",
    description="A task management system built with Hexagonal Architecture",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)
app.include_router(projects.router)


@app.get("/", tags=["health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Task Management System",
        "version": "1.0.0",
        "architecture": "Hexagonal (Ports & Adapters)"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "connected",
        "event_bus": "active",
        "config": {
            "auto_complete_project": settings.AUTO_COMPLETE_PROJECT,
            "log_level": settings.LOG_LEVEL
        }
    }