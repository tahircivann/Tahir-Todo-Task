# FastAPI Task Management System

A robust, scalable task management system built with FastAPI following Clean Architecture principles. This application provides a comprehensive REST API for managing projects and tasks with proper separation of concerns and extensive testing.

## 🏗️ Architecture

This project implements **Clean Architecture** with the following layers:

- **Domain Layer**: Core business entities, events, and rules
- **Application Layer**: Business logic orchestration and services
- **Infrastructure Layer**: Database, external services, and configuration
- **API Layer**: FastAPI endpoints, schemas, and dependency injection

## ✨ Features

- **Project Management**: Create, read, update, and delete projects
- **Task Management**: Full CRUD operations for tasks within projects
- **Clean Architecture**: Proper separation of concerns and dependency inversion
- **Event-Driven**: Domain events for loose coupling between components
- **Comprehensive Testing**: Unit and integration tests with pytest
- **Docker Support**: Containerized deployment with Docker and docker-compose
- **Database Integration**: SQLAlchemy ORM with SQLite database
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/tahircivann/Tahir-Todo-Task.git
   cd Tahir-Todo-Task
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Run the application**
   ```bash
   uvicorn src.api.main:app --reload
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Interactive API docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test types
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start the application
docker-compose up --build

# Run in detached mode
docker-compose up -d --build
```

### Using Docker directly

```bash
# Build the image
docker build -t task-management-api .

# Run the container
docker run -p 8000:8000 task-management-api
```

## 📚 API Endpoints

### Projects
- `GET /projects` - List all projects
- `POST /projects` - Create a new project
- `GET /projects/{project_id}` - Get project details
- `PUT /projects/{project_id}` - Update a project
- `DELETE /projects/{project_id}` - Delete a project

### Tasks
- `GET /projects/{project_id}/tasks` - List tasks in a project
- `POST /projects/{project_id}/tasks` - Create a new task
- `GET /projects/{project_id}/tasks/{task_id}` - Get task details
- `PUT /projects/{project_id}/tasks/{task_id}` - Update a task
- `DELETE /projects/{project_id}/tasks/{task_id}` - Delete a task

## 🏛️ Project Structure

```
src/
├── api/                    # FastAPI application layer
│   ├── routers/           # API endpoints
│   ├── schemas/           # Pydantic models
│   └── dependencies.py    # Dependency injection
├── application/           # Business logic orchestration
│   ├── services/          # Application services
│   ├── event_handlers/    # Domain event handlers
│   └── ports/             # Interfaces/contracts
├── domain/                # Core business logic
│   ├── entities/          # Domain entities
│   ├── events/            # Domain events
│   └── exceptions/        # Domain exceptions
└── infrastructure/        # External concerns
    ├── database/          # Database models and repositories
    ├── config/            # Application configuration
    └── event_bus/         # Event bus implementation

tests/                     # Test suite
├── unit/                  # Unit tests
├── integration/           # Integration tests
└── conftest.py           # Test configuration
```

## 🛠️ Development

### Setting up the development environment

1. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests to ensure everything is working:
   ```bash
   pytest
   ```

3. Start the development server with auto-reload:
   ```bash
   uvicorn src.api.main:app --reload
   ```

### Code Quality

This project follows Python best practices:
- Type hints throughout the codebase
- Clean Architecture principles
- Comprehensive test coverage
- Proper error handling
- Event-driven architecture

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Tahir Civan**
- GitHub: [@tahircivann](https://github.com/tahircivann)

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- SQLAlchemy for the ORM
- Pytest for the testing framework
- Clean Architecture principles by Robert C. Martin

---

⭐ If you found this project helpful, please give it a star!
