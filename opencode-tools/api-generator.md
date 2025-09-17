# 🔧 API Generator
*OpenCode Native Tool - Conversational API Development*

📝 **Conversational Interface** | 🤖 **Context-Aware** | 🔄 **Progressive Development**

## What Makes This Different
Unlike template-based API generators, this tool **conversations with you** to build APIs that integrate seamlessly with your existing codebase.

## How to Use
Simply describe what you need in natural language:

### Conversation Starters
- "I need a user management API for my FastAPI app"
- "Add authentication endpoints to my existing Express server"
- "Create a GraphQL API for my e-commerce database"
- "Help me build a REST API that connects to my PostgreSQL database"

### Example Conversation
**You**: "I need an API for managing blog posts"
**OpenCode**: "I see you have a Django project. Should I add blog post models with user relationships? I noticed you're using PostgreSQL - I can create the migrations too."

**You**: "Yes, and add comment functionality"
**OpenCode**: "Perfect! I'll add Post and Comment models with proper relationships. Should comments support threading/replies? I'll also add moderation features."

**You**: "Add image uploads for posts"
**OpenCode**: "Great! I'll integrate with your existing media settings and add image validation. Should I include thumbnail generation and CDN integration?"

## Framework Selection Matrix

### FastAPI (Python)
**Best for:** High performance, async operations, type safety, modern Python
**Use cases:** Microservices, Data APIs, ML APIs, Real-time systems
**Stack:** FastAPI + Pydantic + SQLAlchemy + PostgreSQL

### Django REST Framework
**Best for:** Rapid development, ORM integration, admin interface, large teams
**Use cases:** CRUD applications, Content management, Enterprise systems
**Stack:** Django + DRF + PostgreSQL + Redis

### Express.js (Node.js)
**Best for:** Node ecosystem, real-time features, frontend integration
**Use cases:** Real-time apps, API gateways, Serverless functions
**Stack:** Express + TypeScript + Prisma + PostgreSQL

### Spring Boot (Java)
**Best for:** Enterprise applications, complex business logic, microservices
**Use cases:** Enterprise APIs, Financial systems, Complex microservices
**Stack:** Spring Boot + JPA + PostgreSQL + Redis

## Implementation Workflow

### 1. Framework Detection
- Analyze existing project structure for framework clues
- Check package.json, requirements.txt, pom.xml, Cargo.toml
- Detect existing database connections and ORM usage
- Identify authentication patterns already in use

### 2. Project Structure Setup
Create appropriate directory structure:

**FastAPI Structure:**
```
app/
├── main.py
├── core/
│   ├── config.py
│   ├── security.py
│   └── database.py
├── api/v1/
│   ├── endpoints/
│   └── deps.py
├── models/
├── schemas/
├── services/
└── tests/
```

**Express.js Structure:**
```
src/
├── index.ts
├── config/
├── middleware/
├── controllers/
├── services/
├── models/
├── types/
└── tests/
```

### 3. Core Components

#### Configuration Management
- Environment variable handling
- Database connection strings
- JWT secrets and security settings
- Rate limiting and CORS configuration

#### Authentication & Security
- JWT token generation and validation
- Password hashing (bcrypt/argon2)
- Rate limiting middleware
- CORS and security headers
- Input validation and sanitization

#### Database Integration
- ORM/ODM setup (SQLAlchemy, Prisma, JPA)
- Migration system configuration
- Connection pooling
- Query optimization patterns

#### API Endpoints
- RESTful route structure
- CRUD operations with proper HTTP methods
- Error handling and status codes
- Request/response validation
- Pagination and filtering

#### Testing Framework
- Unit tests for services and utilities
- Integration tests for endpoints
- Test database setup
- Authentication testing
- Load testing configuration

### 4. Production Features

#### Monitoring & Observability
- Health check endpoints
- Prometheus metrics collection
- Structured logging with correlation IDs
- Error tracking and alerting

#### Performance Optimization
- Response caching strategies
- Database query optimization
- API response compression
- Connection pooling tuning

#### Security Hardening
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- Rate limiting per user/IP
- Security headers implementation

### 5. Deployment Configuration

#### Docker Setup
- Multi-stage builds for optimization
- Non-root user configuration
- Health checks and graceful shutdown
- Environment-specific configurations

#### CI/CD Pipeline
- Automated testing on multiple environments
- Security scanning (bandit, safety, snyk)
- Code quality checks (linting, formatting)
- Container image building and pushing

## Integration Patterns

### Database-First Development
1. Analyze existing database schema
2. Generate models from existing tables
3. Create API endpoints based on data relationships
4. Implement business logic around data operations

### API-First Development
1. Define OpenAPI/Swagger specification
2. Generate models and validation schemas
3. Implement endpoint handlers
4. Add business logic and data persistence

### Microservices Architecture
1. Domain-driven service boundaries
2. Service discovery and communication
3. Distributed tracing and monitoring
4. Event-driven architecture patterns

## 🌟 OpenCode Advantages

### Intelligent Integration
- **Codebase Awareness**: Automatically detects your existing framework, database, and patterns
- **Incremental Building**: Adds features to existing projects without breaking changes
- **Smart Suggestions**: Recommends complementary features based on your current setup
- **Real-time Adaptation**: Adjusts implementation based on your feedback during development

### Natural Development Flow
- **No Command Syntax**: Just describe what you need in plain English
- **Progressive Feature Building**: Start simple, add complexity through conversation
- **Context Preservation**: Remembers decisions made earlier in the conversation
- **Intelligent Defaults**: Uses sensible defaults based on your existing code patterns

### Framework Auto-Detection
```python
def detect_framework():
    """Detect existing framework from project structure"""
    if os.path.exists("requirements.txt"):
        with open("requirements.txt") as f:
            content = f.read()
            if "fastapi" in content:
                return "fastapi"
            elif "django" in content:
                return "django"
    elif os.path.exists("package.json"):
        with open("package.json") as f:
            data = json.load(f)
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            if "express" in deps:
                return "express"
    elif os.path.exists("pom.xml"):
        return "spring_boot"
    
    return None  # Prompt user for framework choice
```

### Progressive Enhancement
1. Start with basic CRUD operations
2. Add authentication when requested
3. Enhance with caching, monitoring, testing
4. Scale to microservices architecture as needed

## Security Best Practices

### Authentication
- JWT tokens with proper expiration
- Refresh token rotation
- Multi-factor authentication support
- OAuth2/OIDC integration patterns

### Data Protection
- Input validation on all endpoints
- SQL injection prevention
- XSS protection for any HTML output
- Sensitive data encryption at rest

### API Security
- Rate limiting per user and globally
- CORS configuration for frontend integration
- API versioning for backward compatibility
- Request/response logging for audit trails

## Testing Strategy

### Test Pyramid
1. **Unit Tests:** Services, utilities, models (70%)
2. **Integration Tests:** API endpoints, database operations (20%)
3. **End-to-End Tests:** Complete user workflows (10%)

### Test Configuration
```python
# FastAPI test setup
@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def test_db():
    # Setup test database
    engine = create_engine("sqlite:///./test.db")
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
```

## Deployment Options

### Container Deployment
- Docker Compose for local development
- Kubernetes manifests for production
- Health checks and resource limits
- Secrets management integration

### Serverless Deployment
- AWS Lambda with API Gateway
- Vercel Functions for Node.js APIs
- Google Cloud Functions
- Environment-specific optimizations

## Success Metrics

### Performance Benchmarks
- Response time < 200ms for CRUD operations
- Throughput > 1000 requests/second
- Database connection efficiency > 95%
- Error rate < 0.1%

### Code Quality Metrics
- Test coverage > 80%
- Code complexity score < 10
- Security vulnerability score: 0 critical
- Documentation coverage > 90%

This OpenCode-adapted version provides the same comprehensive API generation capabilities while working within OpenCode's single-agent architecture and direct conversation model.