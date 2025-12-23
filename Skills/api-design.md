# Skill: API Design
Version: 1.0.0
Category: Development
Tags: [api, rest, graphql, design, architecture]
Prerequisites: [project-genesis]

## Purpose
Design and implement production-ready APIs with best practices for security, performance, and maintainability.

## Triggers
- "Design an API for..."
- "Create REST endpoints"
- "Build GraphQL schema"
- "API architecture"

## Workflow

### Phase 1: API Strategy
1. **Choose API Style**
   ```
   Decision Tree:
   ├── REST - Standard CRUD, broad compatibility
   ├── GraphQL - Complex queries, mobile apps
   ├── gRPC - High performance, microservices
   └── WebSocket - Real-time, bidirectional
   ```

2. **Define Resources**
   - Identify entities
   - Map relationships
   - Define actions

3. **Version Strategy**
   - URL path: `/api/v1/resource`
   - Header: `Accept: application/vnd.api+json;version=1`
   - Query: `/api/resource?version=1`

### Phase 2: Design Principles

#### RESTful Design
```yaml
# Resource naming
/api/v1/users          # Collection
/api/v1/users/{id}     # Single resource
/api/v1/users/{id}/posts  # Nested resource

# HTTP Methods
GET     - Read
POST    - Create
PUT     - Full update
PATCH   - Partial update
DELETE  - Remove

# Status codes
200 - OK
201 - Created
204 - No content
400 - Bad request
401 - Unauthorized
403 - Forbidden
404 - Not found
429 - Rate limited
500 - Server error
```

#### GraphQL Schema
```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}

type Query {
  user(id: ID!): User
  users(limit: Int = 10): [User!]!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
}
```

### Phase 3: Security Implementation

1. **Authentication**
   ```python
   # JWT Bearer token
   headers = {
       "Authorization": "Bearer eyJhbGc..."
   }

   # API Key
   headers = {
       "X-API-Key": "sk_live_..."
   }
   ```

2. **Rate Limiting**
   ```python
   # Per endpoint limits
   RATE_LIMITS = {
       "GET /api/users": "1000/hour",
       "POST /api/users": "100/hour",
       "DELETE /api/users/*": "10/hour"
   }
   ```

3. **Input Validation**
   ```python
   from pydantic import BaseModel, validator

   class UserCreate(BaseModel):
       email: str
       password: str
       name: str

       @validator('email')
       def validate_email(cls, v):
           # Email validation logic
           return v

       @validator('password')
       def validate_password(cls, v):
           if len(v) < 8:
               raise ValueError('Password too short')
           return v
   ```

### Phase 4: Performance Optimization

1. **Pagination**
   ```json
   {
     "data": [...],
     "pagination": {
       "page": 1,
       "per_page": 20,
       "total": 200,
       "pages": 10
     }
   }
   ```

2. **Field Selection**
   ```
   GET /api/users?fields=id,name,email
   ```

3. **Caching Strategy**
   ```python
   # Cache headers
   headers = {
       "Cache-Control": "public, max-age=3600",
       "ETag": "\"33a64df551\"",
       "Last-Modified": "Wed, 21 Oct 2024 07:28:00 GMT"
   }
   ```

### Phase 5: Documentation

1. **OpenAPI/Swagger**
   ```yaml
   openapi: 3.0.0
   info:
     title: My API
     version: 1.0.0
   paths:
     /users:
       get:
         summary: List users
         responses:
           200:
             description: Success
   ```

2. **API Client SDKs**
   - Python client
   - JavaScript client
   - Go client

3. **Interactive Documentation**
   - Swagger UI
   - Postman collection
   - GraphQL playground

### Phase 6: Testing Strategy

1. **Unit Tests**
   ```python
   def test_create_user():
       response = client.post("/api/users", json={
           "name": "Test User",
           "email": "test@example.com"
       })
       assert response.status_code == 201
       assert response.json()["id"] is not None
   ```

2. **Integration Tests**
   - Database connections
   - External services
   - Authentication flow

3. **Load Testing**
   ```bash
   # Using k6
   k6 run --vus 100 --duration 30s load_test.js
   ```

## Inputs Required
- **API Purpose**: What problem it solves
- **Resource Types**: Main entities
- **Client Types**: Web, mobile, M2M
- **Performance Needs**: RPS, latency
- **Security Level**: Public, private, restricted

## Expected Outputs
- API specification (OpenAPI/GraphQL schema)
- Implementation code
- Security configuration
- Test suite
- Documentation
- Client SDKs
- Monitoring setup

## Success Metrics
- ✅ All endpoints documented
- ✅ Authentication working
- ✅ Rate limiting active
- ✅ Tests passing (>80% coverage)
- ✅ Response time <200ms (p95)
- ✅ Zero security vulnerabilities

## Common Pitfalls
- **Over-fetching**: Use pagination and field selection
- **Under-fetching**: Consider GraphQL or includes
- **Inconsistent naming**: Stick to one convention
- **Missing versioning**: Plan for changes
- **Poor errors**: Provide actionable error messages
- **No rate limits**: Prevent abuse from day one

## FastAPI Example
```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import asyncpg

app = FastAPI(title="My API", version="1.0.0")

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@app.get("/api/v1/users", response_model=List[UserResponse])
async def get_users(
    limit: int = 10,
    offset: int = 0,
    db = Depends(get_db)
):
    """Get paginated list of users"""
    users = await db.fetch(
        "SELECT * FROM users LIMIT $1 OFFSET $2",
        limit, offset
    )
    return users

@app.post("/api/v1/users", response_model=UserResponse, status_code=201)
async def create_user(
    user: UserCreate,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new user"""
    result = await db.fetchrow(
        "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *",
        user.name, user.email
    )
    return UserResponse(**result)
```

## Related Skills
- `/skill auth-implementation` - Authentication patterns
- `/skill database-design` - Data layer
- `/skill testing-strategy` - Test coverage
- `/skill monitoring-setup` - Observability

## Neural Database Patterns
- `api_design_[project]` - Design decisions
- `api_performance_[endpoint]` - Performance metrics
- `api_errors_[type]` - Error patterns and fixes
- `api_evolution_[version]` - Version migrations