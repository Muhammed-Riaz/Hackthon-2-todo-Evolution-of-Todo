# Chat Feature Documentation

## Overview
The chat feature provides an AI-powered interface for managing Todo tasks through natural language conversations. Users can interact with the AI assistant to create, update, and manage their tasks using conversational commands.

## Architecture
- **Frontend**: Next.js 14+ with App Router
- **UI Library**: OpenAI ChatKit-like interface (custom implementation)
- **Authentication**: Better Auth with JWT tokens
- **Backend**: FastAPI API at `/api/{user_id}/chat`
- **State Management**: React Context API

## Components

### ChatProvider
- Manages conversation state (messages, conversation_id)
- Handles API communication with backend
- Provides context to child components

### ChatView
- Main chat UI component
- Renders message bubbles and input area
- Provides "New Chat" button for starting fresh conversations

### ChatPage
- Protected route requiring authentication
- Initializes the chat interface
- Redirects unauthenticated users to login

## API Integration
- POST `/api/{user_id}/chat` for sending messages
- Automatic JWT token injection
- Error handling and user feedback

## Features
- Real-time conversation with AI assistant
- Conversation continuity within sessions
- Loading indicators during API requests
- Error handling and recovery
- Accessibility features (ARIA labels, semantic HTML)
- Responsive design for different screen sizes

## Usage
1. User navigates to `/chat` route
2. Authentication is verified
3. Chat interface loads with conversation history
4. User types message and submits
5. Message is sent to backend AI agent
6. Assistant response is displayed
7. Conversation continues with back-and-forth exchanges

## Authentication
- JWT tokens are automatically included in API requests
- User sessions are validated before accessing chat
- Unauthenticated access is redirected to login

## State Management
- Conversation state is maintained per session
- Messages include timestamps and status indicators
- Conversation ID is managed across requests
- New conversation functionality available

## Error Handling
- Network errors are caught and displayed
- API errors are shown to users
- Graceful degradation when backend is unavailable
- Recovery options provided

## Accessibility
- Semantic HTML elements used
- ARIA labels for screen readers
- Keyboard navigation support
- Proper focus management
- Color contrast compliant with WCAG