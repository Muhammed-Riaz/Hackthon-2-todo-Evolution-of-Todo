# Quickstart Guide: Backend Core & Data Layer

**Feature**: 001-backend-core-data

## Setup Instructions

### Prerequisites
- Python 3.11+
- pip package manager
- Git
- Neon Serverless PostgreSQL account

### Installation Steps

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   git checkout 001-backend-core-data
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn sqlmodel pydantic-settings psycopg2-binary python-multipart
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file with your Neon PostgreSQL connection details:
   ```
   DATABASE_URL=postgresql+psycopg2://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname
   ```

5. **Initialize the database** (if using Alembic for migrations):
   ```bash
   # Run migrations to create tables
   alembic upgrade head
   ```

   Or if auto-creation is configured:
   ```bash
   # Start the application to create tables
   python -m backend.src.main
   ```

## Running the Application

1. **Start the development server**:
   ```bash
   cd backend
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the API**:
   - API Documentation: http://localhost:8000/docs
   - API Redoc: http://localhost:8000/redoc

## API Usage Examples

### Create a Task
```bash
curl -X POST "http://localhost:8000/api/user123/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, bread, eggs"}'
```

### List User Tasks
```bash
curl -X GET "http://localhost:8000/api/user123/tasks"
```

### Get a Specific Task
```bash
curl -X GET "http://localhost:8000/api/user123/tasks/1"
```

### Update a Task
```bash
curl -X PUT "http://localhost:8000/api/user123/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries (updated)", "completed": true}'
```

### Complete a Task
```bash
curl -X PATCH "http://localhost:8000/api/user123/tasks/1/complete"
```

### Delete a Task
```bash
curl -X DELETE "http://localhost:8000/api/user123/tasks/1"
```

## Testing the API

### Manual Testing
- Use the interactive API documentation at http://localhost:8000/docs
- Use curl or Postman to test endpoints directly

### Verification Steps
1. Create a task and verify it's returned in the list
2. Update a task and verify changes persist
3. Mark a task as complete and verify the status
4. Delete a task and verify it's removed
5. Verify user isolation by testing with different user_ids

## Project Structure
```
backend/
├── src/
│   ├── models/
│   │   └── task_model.py        # SQLModel definitions
│   ├── schemas/
│   │   └── task_schemas.py      # Pydantic schemas for API
│   ├── api/
│   │   └── v1/
│   │       └── routes/
│   │           └── tasks.py     # Task CRUD endpoints
│   ├── database/
│   │   ├── __init__.py
│   │   ├── database.py          # Database connection/session management
│   │   └── engine.py            # Database engine configuration
│   ├── core/
│   │   └── config.py            # Configuration and environment variables
│   ├── services/
│   │   └── task_service.py      # Business logic for task operations
│   └── main.py                  # FastAPI application entry point
├── requirements.txt
├── alembic.ini                 # Database migration configuration
├── .env.example               # Example environment variables
└── .env                       # Environment variables (gitignored)
```

## Troubleshooting

### Common Issues
- **Database Connection**: Verify your Neon PostgreSQL connection string is correct in `.env`
- **Missing Tables**: Run migrations or ensure auto-creation is enabled
- **Port Already in Use**: Change the port in the uvicorn command
- **Import Errors**: Ensure all dependencies are installed in your virtual environment

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `ENVIRONMENT`: Set to "development", "staging", or "production"
- `LOG_LEVEL`: Logging level (debug, info, warning, error)