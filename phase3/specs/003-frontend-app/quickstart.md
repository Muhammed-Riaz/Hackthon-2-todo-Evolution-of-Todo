# Quickstart Guide: Frontend Application (Next.js + Better Auth)

## Development Setup

### Prerequisites
- Node.js 18+ installed
- Access to the secured FastAPI backend
- Better Auth configured with JWT support
- Environment variables configured (NEXT_PUBLIC_API_URL, NEXT_PUBLIC_BETTER_AUTH_URL)

### Installation Steps

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create environment file:
   ```bash
   cp .env.example .env.local
   ```

4. Update environment variables in `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
   ```

5. Start the development server:
   ```bash
   npm run dev
   ```

## Running the Application

### Development Mode
```bash
npm run dev
```
Application will be available at `http://localhost:3000`

### Production Build
```bash
npm run build
npm run start
```

## Key Features Walkthrough

### Authentication Flow
1. Visit `/login` or `/signup` to authenticate
2. Better Auth handles user registration/login
3. JWT token is automatically stored and used for API calls
4. User is redirected to dashboard after authentication

### Task Management
1. Once authenticated, navigate to `/dashboard/tasks`
2. View all tasks associated with the current user
3. Create new tasks using the "Add Task" button
4. Edit, delete, or mark tasks as complete using action buttons
5. All operations are secured with JWT authentication

### API Integration
- All API calls automatically include the JWT token in headers
- Error handling provides user feedback for failed operations
- Loading states provide visual feedback during API calls

## Testing the Application

### Manual Testing Steps

1. **Authentication Testing**:
   - Navigate to `/signup` and create a new account
   - Verify you're redirected to the dashboard
   - Log out and verify access to protected routes is blocked

2. **Task Management Testing**:
   - Create a new task and verify it appears in the list
   - Edit an existing task and verify changes persist
   - Mark a task as complete and verify the status updates
   - Delete a task and verify it's removed from the list

3. **Security Testing**:
   - Attempt to access protected routes without authentication
   - Verify that users can only see their own tasks
   - Test JWT token expiration handling

4. **Responsive Testing**:
   - Resize browser window to test mobile responsiveness
   - Verify all functionality works on different screen sizes

## Troubleshooting

### Common Issues

1. **API Connection Issues**:
   - Verify backend server is running
   - Check that API URL is correctly set in environment variables
   - Ensure JWT token is being sent with requests

2. **Authentication Issues**:
   - Verify Better Auth is properly configured
   - Check that JWT secret matches between frontend and backend
   - Clear browser storage if authentication state becomes corrupted

3. **Component Rendering Issues**:
   - Check browser console for JavaScript errors
   - Verify all required props are passed to components
   - Ensure API responses match expected data structure

### Environment Variables
- `NEXT_PUBLIC_API_URL`: Base URL for the backend API
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Base URL for Better Auth
- `NEXT_PUBLIC_JWT_SECRET`: Secret used for JWT verification (should match backend)

## Deployment Notes

### Environment Configuration
- Update API URLs to production endpoints
- Configure proper JWT secrets for production
- Set up SSL certificates for secure connections

### Build Optimization
- The application is optimized for production builds
- Images and assets are automatically optimized
- Code splitting is enabled for faster loading

## API Interaction Examples

### Making Authenticated API Calls
```javascript
import { api } from '../services/api-client';

// Get user's tasks
const tasks = await api.get(`/api/${userId}/tasks`);

// Create a new task
const newTask = await api.post(`/api/${userId}/tasks`, {
  title: 'New Task',
  description: 'Task description'
});
```

### Error Handling
```javascript
try {
  const result = await api.get('/api/user/tasks');
  // Handle successful response
} catch (error) {
  // Handle error response
  console.error('API call failed:', error.message);
}
```