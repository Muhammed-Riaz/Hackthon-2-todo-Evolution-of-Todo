# Todo Full-Stack Web Application (Phase II)

A modern, secure, multi-user todo application built with Next.js, FastAPI, and PostgreSQL.

## Features

- **User Authentication**: Secure registration and login with JWT tokens
- **Task Management**: Create, read, update, and delete tasks
- **Multi-user Isolation**: Each user can only access their own tasks
- **Responsive UI**: Works on desktop and mobile devices
- **Persistent Storage**: Data stored in Neon Serverless PostgreSQL

## Tech Stack

- **Frontend**: Next.js 16+ with App Router
- **Backend**: Python FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT tokens
- **Styling**: Tailwind CSS

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login a user
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - Logout the user

### Task Management
- `GET /api/v1/users/{user_id}/tasks` - Get all tasks for a user
- `POST /api/v1/users/{user_id}/tasks` - Create a new task
- `GET /api/v1/users/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/v1/users/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/v1/users/{user_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/v1/users/{user_id}/tasks/{task_id}/complete` - Toggle task completion

## Security Features

- JWT token authentication for all API requests
- User isolation - users can only access their own data
- Passwords are securely hashed using bcrypt
- Automatic token expiration

## Project Structure

```
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application entry point
│   ├── models/             # Database models
│   │   └── user_task_models.py
│   ├── api/                # API routes
│   │   └── v1/
│   │       └── routers/
│   │           ├── auth.py
│   │           └── tasks.py
│   ├── utils/              # Utility functions
│   │   └── auth.py
│   ├── database.py         # Database configuration
│   ├── settings.py         # Application settings
│   └── requirements.txt
├── frontend/               # Next.js frontend
│   ├── app/                # App Router pages
│   │   ├── api/            # API routes
│   │   │   └── auth/
│   │   ├── login/          # Login page
│   │   ├── register/       # Registration page
│   │   └── page.tsx        # Home page
│   ├── components/         # React components
│   │   ├── auth-provider.tsx
│   │   └── navbar.tsx
│   ├── contexts/           # React contexts
│   │   └── todo-context.tsx
│   ├── lib/                # Library functions
│   │   ├── auth.ts
│   │   └── api-client.ts
│   ├── types/              # TypeScript types
│   │   └── task.ts
│   ├── package.json
│   ├── next.config.js
│   └── app/
├── specs/                  # Specifications
│   └── 001-todo-web-app/
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── .specify/               # Claude Code configuration
├── CLAUDE.md               # Claude Code instructions
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Start the backend server:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
# Edit .env.local with your configuration
```

4. Start the development server:
```bash
npm run dev
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-super-secret-jwt-token-with-at-least-32-characters-long
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
BETTER_AUTH_SECRET=your-super-secret-jwt-token-with-at-least-32-characters-long
BETTER_AUTH_URL=http://localhost:8000
```

## Running Tests

To run the multi-user isolation tests:

```bash
cd backend
python -m pytest test_multi_user_isolation.py -v
```

## Development

The project follows a spec-driven development approach with the following workflow:
1. Write spec → Generate plan → Break into tasks → Implement via Claude Code
2. All changes are tracked in the spec-kit plus workflow
3. Each feature has complete documentation in the specs directory

## Security Considerations

- All API endpoints require valid JWT tokens
- User data is isolated at the database level
- Passwords are securely hashed using bcrypt
- JWT tokens have appropriate expiration times
- Input validation is implemented for all endpoints

## Deployment

### GitHub Pages Deployment

This application is configured for deployment to GitHub Pages:

1. The frontend is configured for static export in `next.config.ts`
2. A GitHub Actions workflow is set up in `.github/workflows/github-pages.yml`
3. Once you push to the `main` branch, the workflow will automatically build and deploy the frontend to GitHub Pages

To configure GitHub Pages deployment:
1. Go to your repository settings
2. Navigate to "Pages" section
3. Under "Source", select "Deploy from a branch"
4. Select "gh-pages" as the branch and "/ (root)" as the folder
5. Your site will be deployed to `https://<username>.github.io/<repository-name>/`

Note: For full functionality, the backend is deployed on Hugging Face at https://riaz110-todo.hf.space. The `NEXT_PUBLIC_API_URL` in `.env.production` is already configured to point to this backend API. The GitHub Pages frontend will communicate with this external backend API.

### Self-Hosting

For production deployment:
1. Set up Neon Serverless PostgreSQL
2. Configure environment variables securely
3. Build the frontend: `npm run build`
4. Deploy both frontend and backend to your preferred hosting platform