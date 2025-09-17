# 🔧 Step-by-Step Guide: Using OpenCode Tools

## Overview
OpenCode tools use **conversational development** to build features that integrate seamlessly with your existing codebase. No commands to memorize - just describe what you need!

## Getting Started: API Generator Example

### Step 1: Start the Conversation
Simply describe what you need in natural language. **No commands to memorize!**

#### Example Conversation Flow

**Step 1: Initial Request**
```
You: "I need a user management API for my web application"
```

**Step 2: OpenCode Analyzes Your Project**
```
OpenCode: "I see you have a FastAPI project with SQLAlchemy already set up. 
Should I add user registration, authentication, and profile management? 
I noticed you're using PostgreSQL - I can integrate with your existing database setup."
```

**Step 3: Clarify Requirements**
```
You: "Yes, and I need JWT authentication with password reset functionality"
```

**Step 4: Progressive Building**
```
OpenCode: "Perfect! I'll create:
- User model with proper password hashing
- JWT token generation and validation
- Registration/login endpoints
- Password reset with email tokens
- Profile management endpoints

Should I also add role-based permissions and email verification?"
```

**Step 5: Iterative Enhancement**
```
You: "Add email verification, but skip roles for now"

OpenCode: "Great! I'll implement email verification with secure tokens. 
Let me start by creating the user model..."
```

### Step 2: What Happens Behind the Scenes

#### 🤖 Automatic Detection
The tool automatically:
- **Detects your framework** (FastAPI, Django, Express, etc.)
- **Analyzes existing code** patterns and structure
- **Identifies database** setup and ORM usage
- **Finds authentication** patterns already in use

#### 🔍 Context Analysis
```python
# OpenCode automatically detects:
project_context = {
    'framework': 'FastAPI',
    'database': 'PostgreSQL + SQLAlchemy', 
    'existing_auth': 'JWT tokens detected',
    'project_structure': 'Standard FastAPI layout',
    'dependencies': ['pydantic', 'sqlalchemy', 'passlib']
}
```

#### 🏗️ Progressive Implementation
1. **Models**: Creates user models that integrate with existing database
2. **Schemas**: Adds Pydantic schemas for validation
3. **Endpoints**: Implements REST endpoints following your project's patterns
4. **Security**: Adds JWT authentication matching your existing setup
5. **Tests**: Creates tests that work with your testing framework

### Step 3: Real Example Implementation

Let's say you have an existing FastAPI project and want to add user management:

#### Your Request:
```
"Add user registration and login to my FastAPI app"
```

#### OpenCode's Response:
```
I'll add user management to your FastAPI application. I see you're already using:
- SQLAlchemy for database operations
- Pydantic for data validation
- PostgreSQL as your database

Let me create the user management system that integrates seamlessly.
```

#### What Gets Created:

**1. User Model (`app/models/user.py`)**
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

**2. Pydantic Schemas (`app/schemas/user.py`)**
```python
from pydantic import BaseModel, EmailStr, validator

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class User(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    
    class Config:
        orm_mode = True
```

**3. API Endpoints (`app/api/v1/endpoints/auth.py`)**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, User
from app.services.auth import AuthService

router = APIRouter()

@router.post("/register", response_model=User)
async def register(user_data: UserCreate, auth_service: AuthService = Depends()):
    return auth_service.create_user(user_data)

@router.post("/login")
async def login(email: str, password: str, auth_service: AuthService = Depends()):
    token = auth_service.authenticate_user(email, password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
```

### Step 4: Continuous Refinement

#### Add More Features Through Conversation:
```
You: "Add password reset functionality"

OpenCode: "I'll add password reset with secure email tokens. Should I:
- Use your existing email service or set up SMTP?
- Set token expiration to 1 hour?
- Add rate limiting to prevent abuse?"

You: "Use SMTP with 30-minute expiration and rate limiting"

OpenCode: "Perfect! I'll implement:
- Password reset request endpoint
- Secure token generation with 30-min expiry
- Email service integration with SMTP
- Rate limiting (3 requests per hour per email)
- Reset confirmation endpoint"
```

### Step 5: Testing and Validation

#### OpenCode Automatically Creates Tests:
```python
# tests/test_auth.py
def test_user_registration(client, db):
    response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

def test_user_login(client, test_user):
    response = client.post("/api/v1/auth/login", data={
        "username": test_user.email,
        "password": "testpassword123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
```

## Using Other OpenCode Tools

### 🛡️ Security Auditor Example

#### Your Request:
```
"Check my API for security vulnerabilities before deployment"
```

#### OpenCode's Analysis:
```
I'll scan your FastAPI application for security issues. I see you're using:
- JWT authentication
- PostgreSQL database
- Password hashing with bcrypt

Let me check for:
- SQL injection vulnerabilities
- Authentication bypass issues
- Exposed secrets or credentials
- Missing security headers
- Dependency vulnerabilities
```

#### Interactive Security Review:
```
OpenCode: "I found a few issues:
1. Your /users endpoint returns password hashes (data exposure)
2. Missing rate limiting on login endpoint
3. One outdated dependency with known vulnerability

Should I fix the password hash exposure first?"

You: "Yes, and add the rate limiting"

OpenCode: "I'll update the user schema to exclude password hashes and add rate limiting middleware. The dependency issue is in 'requests' - should I update it to the latest secure version?"
```

### 🐳 Container Optimizer (Coming Soon)

#### Your Request:
```
"Optimize my Docker setup for production"
```

#### Expected OpenCode Response:
```
I see you have a Dockerfile for your FastAPI app. I can optimize it by:
- Using multi-stage builds to reduce image size
- Adding non-root user for security
- Optimizing layer caching
- Adding health checks

Your current image is 1.2GB - I can reduce it to ~200MB. Should I proceed?
```

## Key Advantages of OpenCode Tools

### 🎯 **Smart Integration**
- Works with your existing codebase
- Follows your established patterns
- Maintains backward compatibility

### 🔄 **Progressive Development**
- Start simple, add complexity through conversation
- Each feature builds on previous work
- Easy to modify and extend

### 📝 **Natural Interface**
- No commands to memorize
- Describe what you need in plain English
- Ask questions and get contextual answers

### 🤖 **Intelligent Defaults**
- Uses secure patterns by default
- Follows best practices for your framework
- Includes proper error handling and validation

## Quick Start Checklist

### For Any OpenCode Tool:

1. ✅ **Describe your need**: "I need [feature] for my [framework] app"
2. ✅ **Engage in conversation**: Discuss options and requirements
3. ✅ **Review suggestions**: OpenCode analyzes your project and suggests approaches
4. ✅ **Refine implementation**: Add details and additional features
5. ✅ **Test and iterate**: Review generated code and make adjustments

## Common Conversation Starters

### 🔧 API Generator
- "I need a REST API for [domain/feature]"
- "Add authentication to my existing [framework] app"
- "Create GraphQL endpoints for my database"
- "Help me build an API that integrates with [service]"

### 🛡️ Security Auditor
- "Check my application for security vulnerabilities"
- "Audit my authentication system"
- "Review my API endpoints for security issues"
- "Scan for exposed secrets and credentials"

### 🐳 Container Optimizer (Coming Soon)
- "Optimize my Docker setup for production"
- "Reduce my container image size"
- "Add security best practices to my Dockerfile"
- "Set up multi-stage builds for my app"

### ☸️ K8s Deployment Assistant (Coming Soon)
- "Help me deploy to Kubernetes"
- "Create production-ready K8s manifests"
- "Set up monitoring and logging for my deployment"
- "Configure auto-scaling for my application"

### 🧪 Test Framework Builder (Coming Soon)
- "Add comprehensive testing to my project"
- "Create integration tests for my API"
- "Set up automated testing pipeline"
- "Add performance testing for my endpoints"

## Tips for Effective Conversations

### ✅ **Be Specific About Context**
Instead of: "I need an API"
Try: "I need a user management API for my existing FastAPI e-commerce application"

### ✅ **Mention Your Tech Stack**
"I'm using FastAPI with PostgreSQL and already have JWT authentication set up"

### ✅ **Ask for Clarification**
"What security measures should I consider?"
"How does this integrate with my existing database?"

### ✅ **Iterate and Refine**
Start with core functionality, then add features through continued conversation

### ✅ **Request Explanations**
"Why did you choose this approach?"
"What are the security implications of this implementation?"

## Troubleshooting

### If OpenCode Seems Confused:
1. **Provide more context** about your existing project
2. **Specify your framework** and key dependencies
3. **Clarify your goals** and constraints
4. **Ask specific questions** about implementation choices

### If You Want to Change Direction:
- "Actually, let's try a different approach..."
- "Can we modify this to work with [different technology]?"
- "I changed my mind about [feature], can we adjust?"

### If You Need More Details:
- "Can you explain how this works?"
- "What are the security considerations?"
- "How does this integrate with my existing code?"
- "What testing should I add for this?"

---

**Remember**: OpenCode tools are conversational partners, not command-line utilities. The more context and detail you provide, the better they can help you build exactly what you need!