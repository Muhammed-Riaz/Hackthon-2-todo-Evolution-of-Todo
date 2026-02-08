# Research: Backend Core & Data Layer Implementation

**Feature**: 001-backend-core-data

## Decision Log

### 1. SQLModel vs SQLAlchemy Core

**Decision**: SQLModel
**Rationale**: The specification explicitly requires using SQLModel for all database operations. SQLModel combines the power of SQLAlchemy with Pydantic validation, making it ideal for FastAPI applications. It provides type hints, validation, and easy serialization to JSON for API responses.
**Alternatives considered**:
- SQLAlchemy Core: Lower level, requires more boilerplate code
- SQLAlchemy ORM: Good but lacks Pydantic integration
- Tortoise ORM: Async native but less mature

### 2. UUID vs Integer Primary Keys

**Decision**: Integer
**Rationale**: For a todo application, integer primary keys are simpler, more efficient for database indexing, and easier to work with. While UUIDs provide distributed generation capabilities, they're not necessary for this application scope and add complexity without significant benefit.
**Alternatives considered**:
- UUID: More secure (harder to enumerate), but more complex and slightly less efficient

### 3. Sync vs Async Database Sessions

**Decision**: Async
**Rationale**: FastAPI is designed for asynchronous operations and async database sessions will allow better performance under load. All database operations will use async/await patterns for maximum efficiency.
**Alternatives considered**:
- Sync: Simpler but doesn't leverage FastAPI's async capabilities

### 4. Hard Delete vs Soft Delete

**Decision**: Hard Delete
**Rationale**: For a simple todo application, hard deletes are more straightforward and efficient. Soft deletes add complexity with no clear benefit for this use case.
**Alternatives considered**:
- Soft Delete: Allows for recovery of accidentally deleted tasks but adds complexity

### 5. Table Auto-Creation vs Migrations

**Decision**: Migrations
**Rationale**: While auto-creation is simpler, migrations provide better control over database schema changes, versioning, and are more suitable for production environments. Alembic will be used for migration management.
**Alternatives considered**:
- Auto-creation: Simpler for development but not suitable for production

### 6. Environment Configuration

**Decision**: Environment Variables with Pydantic Settings
**Rationale**: Using Pydantic's BaseSettings for configuration provides type validation and structured access to environment variables. This approach is secure and follows FastAPI best practices.
**Alternatives considered**:
- Direct os.environ usage: Less structured and no type validation

### 7. Error Handling Strategy

**Decision**: Custom HTTP Exception Handlers
**Rationale**: FastAPI's built-in exception handling combined with custom handlers will provide consistent error responses across all endpoints. This ensures all API responses follow the same JSON structure.
**Alternatives considered**:
- Manual error handling in each endpoint: Would lead to inconsistent responses

### 8. Request Flow Architecture

**Decision**: API Router → Service Layer → Model Layer
**Rationale**: This layered architecture provides clear separation of concerns. The API router handles HTTP-specific concerns, the service layer contains business logic, and the model layer handles data persistence.
**Alternatives considered**:
- Direct model access from routers: Would mix concerns and reduce testability