# PlantUML Diagrams for Task Management System

This directory contains PlantUML diagrams that explain the architecture, design, and operation of the Task Management System built with Hexagonal Architecture.

## 📁 Diagram Files

### 1. `architecture.puml` - System Architecture Overview
**Purpose**: Shows the overall system architecture using Hexagonal Architecture (Ports & Adapters) pattern.

**What it shows**:
- **API Layer**: FastAPI application with routers and schemas
- **Application Layer**: Services, event handlers, and port interfaces
- **Domain Layer**: Core business entities, events, and exceptions
- **Infrastructure Layer**: Database implementations, event bus, and configuration
- **External Systems**: Client applications and Docker containerization

**Key Features Highlighted**:
- Clean separation of concerns
- Dependency inversion through ports
- Event-driven architecture
- Database abstraction

### 2. `event_flow_sequence.puml` - Event Flow Sequence
**Purpose**: Demonstrates the automatic task deadline adjustment feature through event-driven architecture.

**What it shows**:
- Complete flow from API request to database update
- Event publishing and handling mechanism
- Automatic task deadline adjustment logic
- Database persistence flow

**Key Features Highlighted**:
- Event publishing before database save
- Automatic task deadline adjustment
- Event handler processing
- Data consistency maintenance

### 3. `domain_model.puml` - Domain Model
**Purpose**: Illustrates the core domain entities, their relationships, and business rules.

**What it shows**:
- **Task Entity**: Core task business logic and state management
- **Project Entity**: Project management and completion logic
- **Domain Events**: All event types and their inheritance
- **Domain Exceptions**: Business rule violations
- **Relationships**: Entity associations and event emissions

**Key Features Highlighted**:
- Rich domain model with business logic
- Event-driven state changes
- Business rule enforcement
- Clean domain boundaries

### 4. `deployment.puml` - Deployment Architecture
**Purpose**: Shows how the system is deployed using Docker and accessed by clients.

**What it shows**:
- **Development Environment**: Developer tools and Git repository
- **Docker Container**: Complete application stack
- **Database Schema**: SQLite tables and relationships
- **External Access**: Web browsers, API clients, and documentation

**Key Features Highlighted**:
- Containerized deployment
- SQLite database with UUID support
- RESTful API endpoints
- Interactive documentation

## 🚀 How to Use These Diagrams

### Prerequisites
1. **PlantUML**: Install PlantUML from [plantuml.com](https://plantuml.com/)
2. **IDE Plugin**: Install PlantUML plugin for your IDE (VS Code, IntelliJ, etc.)
3. **Online Viewer**: Use [PlantUML Online Server](http://www.plantuml.com/plantuml/uml/) for quick viewing

### Viewing the Diagrams

#### Option 1: VS Code with PlantUML Extension
1. Install the "PlantUML" extension in VS Code
2. Open any `.puml` file
3. Press `Alt+D` to preview the diagram
4. Use `Ctrl+Shift+P` → "PlantUML: Export Current Diagram" to save as image

#### Option 2: Command Line
```bash
# Generate PNG images
plantuml -tpng *.puml

# Generate SVG images
plantuml -tsvg *.puml

# Generate PDF images
plantuml -tpdf *.puml
```

#### Option 3: Online Viewer
1. Copy the content of any `.puml` file
2. Go to [PlantUML Online Server](http://www.plantuml.com/plantuml/uml/)
3. Paste the content and click "Submit"

### Customizing the Diagrams

#### Colors and Styling
```plantuml
!theme plain
skinparam backgroundColor #FFFFFF
skinparam component {
    BackgroundColor #F3E5F5
    BorderColor #4A148C
}
```

#### Adding Notes
```plantuml
note right of ComponentName
  Your explanation here
end note
```

#### Adding Relationships
```plantuml
ComponentA --> ComponentB : "relationship description"
ComponentA ..> ComponentB : "dotted relationship"
```

## 🏗️ Architecture Patterns Explained

### Hexagonal Architecture (Ports & Adapters)
- **Domain Layer**: Core business logic, independent of external concerns
- **Application Layer**: Use cases and application services
- **Infrastructure Layer**: External concerns (database, web, etc.)
- **Ports**: Interfaces that define contracts
- **Adapters**: Implementations of ports

### Event-Driven Architecture
- **Domain Events**: Represent business state changes
- **Event Bus**: Publishes and routes events
- **Event Handlers**: Process events and trigger side effects
- **Automatic Adjustments**: Business rules enforced through events

### Repository Pattern
- **Repository Interface**: Defines data access contract
- **Repository Implementation**: Concrete implementation using ORM
- **Dependency Inversion**: High-level modules don't depend on low-level modules

## 🔧 System Features Demonstrated

### 1. Automatic Task Deadline Adjustment
When a project deadline is shortened, all tasks with deadlines beyond the new project deadline are automatically adjusted.

### 2. Project Auto-Completion
When all tasks in a project are completed, the project is automatically marked as completed.

### 3. Event-Driven State Management
All state changes emit domain events that can trigger side effects and maintain consistency.

### 4. Clean Architecture
Clear separation of concerns with well-defined boundaries between layers.

## 📚 Additional Resources

- [PlantUML Documentation](https://plantuml.com/)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)

## 🤝 Contributing

When modifying the system architecture:
1. Update the relevant PlantUML diagrams
2. Ensure diagrams reflect the current implementation
3. Add new diagrams for new features or patterns
4. Update this README with new diagram descriptions

---

**Note**: These diagrams are living documentation and should be updated as the system evolves.
