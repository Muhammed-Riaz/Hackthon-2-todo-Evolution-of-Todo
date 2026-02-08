# Quickstart Guide: ChatKit Frontend

## Development Setup

### Prerequisites
- Node.js 18+ installed
- Better Auth configured and running
- Backend chat API at /api/{user_id}/chat available
- Access to Neon PostgreSQL database

### Installation
1. Install ChatKit package:
   ```bash
   npm install @openai/chatkit
   ```

2. Verify existing dependencies:
   ```bash
   npm install
   ```

3. Ensure Better Auth is configured in your Next.js project

### Environment Variables
- NEXT_PUBLIC_API_URL: Backend API base URL
- NEXT_PUBLIC_BETTER_AUTH_URL: Better Auth instance URL

## Running the Application

### Development
1. Start the development server:
   ```bash
   npm run dev
   ```

2. Navigate to `/chat` in your browser

3. Ensure you are logged in (Better Auth session required)

### Testing the Chat Interface
1. Open browser to http://localhost:3000/chat
2. Verify authentication is required
3. Type a message like "Add a task to buy groceries"
4. Press Enter or click Send
5. Verify response appears in chat window
6. Check that conversation_id is maintained for next message

## Component Integration

### Chat Provider State
- Handles conversation_id persistence
- Manages message history in component state
- Coordinates between UI and API client

### API Client
- Located at `/lib/chat/api.ts`
- Makes POST requests to `/api/{user_id}/chat`
- Handles authentication headers automatically
- Returns structured responses with conversation_id

### Auth Integration
- Automatically extracts user_id from Better Auth session
- Adds JWT token to Authorization header
- Redirects to login if session is invalid/expired

## Troubleshooting

### Common Issues
- **401 Unauthorized**: Check that you're logged in and JWT token is valid
- **500 Internal Error**: Verify backend chat API is running
- **Messages not appearing**: Check browser console for JavaScript errors
- **Slow responses**: Verify network connectivity to backend

### Verification Steps
1. Test backend API directly with curl:
   ```bash
   curl -X POST http://localhost:8000/api/{user_id}/chat \
   -H "Authorization: Bearer {token}" \
   -H "Content-Type: application/json" \
   -d '{"message": "test"}'
   ```
2. Check browser developer tools for network errors
3. Verify Better Auth session in browser storage