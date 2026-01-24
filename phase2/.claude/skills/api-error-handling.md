# API Error Handling Skill

**Name:** `api-error-handling`
**Description:** Standardised error handling pattern for FastAPI endpoints and frontend API responses in Phase 2 Todo app
**Version:** `1.0-phase2`

## Instructions

When implementing any API endpoint or frontend fetch call, ALWAYS follow this error handling pattern.

## Backend Pattern (FastAPI)

### Rules
- Use `HTTPException` for expected errors
- Return consistent JSON shape on error
- Log unexpected errors with `logger.exception()`
- Never leak stack traces or database errors to client

### Error Response Shape

```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED | VALIDATION_ERROR | NOT_FOUND | INTERNAL_ERROR",
    "message": "Human readable message",
    "details": {}
  }
}
```

### Example Error Responses

**401 Unauthorized:**
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or missing token"
  }
}
```

**422 Validation Error:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title is required",
    "details": {
      "title": "String should have at least 1 character"
    }
  }
}
```

**404 Not Found:**
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Task not found"
  }
}
```

## Frontend Pattern (Next.js)

### Rules
- Check `response.ok` status
- Try to parse JSON error shape
- Show user-friendly toast/notification
- For 401 → redirect to login
- For 403/404 → show specific message
- For 500 → show generic "Something went wrong" + retry button

## Application Scope

Apply this skill to every endpoint and API interaction in Phase 2 Todo app.