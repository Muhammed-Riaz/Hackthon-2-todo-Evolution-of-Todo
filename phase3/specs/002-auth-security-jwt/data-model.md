# Data Model: Authentication & API Security

**Feature**: 002-auth-security-jwt

## Entities

### User (Existing from Spec 1, Enhanced)

**Description**: Represents a registered user in the system with authentication capabilities

**Fields**:
- `id`: String (Primary Identifier from Better Auth)
- `email`: String (Unique, required)
- `name`: String (Optional)
- `created_at`: DateTime (Auto-generated)
- `updated_at`: DateTime (Auto-generated)

**Authentication Properties**:
- `jwt_token`: String (Issued by Better Auth, stored client-side)
- `token_expires_at`: DateTime (Expiration time of JWT token)

**Relationships**:
- Has many Tasks (via user_id foreign key)

### JWT Token

**Description**: JSON Web Token issued by Better Auth upon successful authentication

**Payload Structure**:
- `sub` (Subject): User identifier (user_id)
- `exp` (Expiration Time): Token expiration timestamp
- `iat` (Issued At): Token issuance timestamp
- `jti` (JWT ID): Unique identifier for the token (optional)
- `user_id`: User identifier (for backward compatibility)
- `email`: User email (optional claim)

**Validation Rules**:
- Must be properly signed with shared secret
- Must not be expired at time of verification
- Signature must match the shared BETTER_AUTH_SECRET
- Subject claim must match the user_id in the request URL

### Authentication Session

**Description**: Stateless authentication session represented by JWT token

**Properties**:
- `token`: String (JWT token string)
- `expires_at`: DateTime (Token expiration time)
- `user_id`: String (Associated user identifier)
- `valid`: Boolean (Whether token is currently valid)

## Security Constraints

### Token Verification
- All API requests must include valid JWT token in Authorization header
- Backend must verify token signature using shared secret
- Token expiration must be validated before processing request
- User identity must be extracted from token payload

### User Isolation
- All task queries must filter by user_id from JWT token
- URL user_id must match JWT token user_id for validation
- Users cannot access resources belonging to other users
- Database queries must enforce user_id scoping regardless of URL parameters

### Secret Management
- BETTER_AUTH_SECRET must be stored in environment variables
- Secret must be the same in both frontend and backend
- Secret must not be exposed in client-side code
- Secret rotation mechanism should be planned for future implementation