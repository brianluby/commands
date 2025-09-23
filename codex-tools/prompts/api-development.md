# 🔧 API Development Prompts for Codex CLI

## Overview
Natural language prompts for creating production-ready APIs using Codex CLI's conversational development approach.

## Core API Development Prompts

### 1. New API Creation

#### FastAPI Application
```bash
codex "Create a FastAPI application for [domain] with the following features:
- [Feature 1]: [Description]
- [Feature 2]: [Description]
- Authentication: [JWT/OAuth/Basic]
- Database: [PostgreSQL/MySQL/MongoDB]
- Include proper error handling, validation, and documentation"
```

**Example:**
```bash
codex "Create a FastAPI application for e-commerce with the following features:
- User management: Registration, login, profile management
- Product catalog: CRUD operations with categories and search
- Shopping cart: Add/remove items, quantity management
- Authentication: JWT with refresh tokens
- Database: PostgreSQL with SQLAlchemy
- Include proper error handling, validation, and OpenAPI documentation"
```

#### Express.js API
```bash
codex "Build an Express.js API for [domain] with TypeScript including:
- [Feature list]
- Authentication: [method]
- Database: [type] with [ORM]
- Middleware: Security headers, CORS, rate limiting
- Testing: Jest with supertest
- Documentation: OpenAPI/Swagger"
```

#### Django REST Framework
```bash
codex "Create a Django REST API for [domain] with:
- Models: [list key models]
- Features: [list key features]
- Authentication: [DRF JWT/OAuth/Token]
- Database: [PostgreSQL/MySQL] 
- Admin interface and API documentation
- Proper serializers and viewsets"
```

### 2. Endpoint Enhancement

#### Add New Endpoints
```bash
codex "Add the following endpoints to my existing [framework] API:
- [HTTP METHOD] /[path] - [description]
- Include proper validation, error handling, and tests
- Follow the existing code patterns and authentication"
```

#### Authentication Integration
```bash
codex "Add JWT authentication to my existing API with:
- User registration and login endpoints
- Password hashing with bcrypt
- Token refresh mechanism
- Protected route middleware
- Rate limiting on auth endpoints"
```

#### Database Integration
```bash
codex "Integrate [database] with my API including:
- Database models for [entities]
- Migration scripts
- Connection pooling and configuration
- CRUD operations with proper error handling
- Database indexing for performance"
```

### 3. API Security

#### Security Hardening
```bash
codex "Harden the security of my API by adding:
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- Rate limiting per user and endpoint
- Security headers (CORS, CSP, HSTS)
- API key authentication for external access"
```

#### Vulnerability Assessment
```bash
codex "Analyze my API for security vulnerabilities and fix:
- Authentication and authorization flaws
- Input validation issues
- Sensitive data exposure
- Improper error handling
- Missing security headers
- Dependency vulnerabilities"
```

### 4. Performance Optimization

#### API Performance
```bash
codex "Optimize my API performance by implementing:
- Response caching with Redis
- Database query optimization
- Connection pooling
- Async operations where appropriate
- Response compression
- API response pagination"
```

#### Load Testing Integration
```bash
codex "Set up load testing for my API including:
- Performance test scripts with [tool]
- Endpoint stress testing
- Database performance under load
- Memory and CPU monitoring
- Performance regression testing in CI"
```

### 5. Testing Strategy

#### Comprehensive Testing
```bash
codex "Create a comprehensive testing strategy for my API including:
- Unit tests for business logic
- Integration tests for database operations
- API endpoint tests with authentication
- Mock external services
- Test fixtures and factories
- CI/CD integration with test coverage reporting"
```

#### Test Data Management
```bash
codex "Set up test data management for my API with:
- Database test fixtures
- Factory patterns for test data generation
- Test database setup and teardown
- Isolated test environments
- Performance test data sets"
```

### 6. Documentation and API Design

#### API Documentation
```bash
codex "Generate comprehensive API documentation including:
- OpenAPI/Swagger specification
- Interactive API explorer
- Authentication examples
- Error response documentation
- SDK generation for [languages]
- Postman collection export"
```

#### API Versioning
```bash
codex "Implement API versioning strategy with:
- URL path versioning (/v1/, /v2/)
- Backward compatibility maintenance
- Version-specific documentation
- Migration guides between versions
- Deprecation notices and timelines"
```

## Advanced Integration Patterns

### 7. Microservices Architecture

#### Service Communication
```bash
codex "Convert my monolithic API into microservices with:
- Service boundaries for [domains]
- Inter-service communication via [REST/gRPC/Events]
- Service discovery and load balancing
- Distributed tracing and monitoring
- API gateway for external access"
```

#### Event-Driven Architecture
```bash
codex "Implement event-driven communication between services:
- Event bus with [technology]
- Async event handlers
- Event sourcing for [entities]
- Saga pattern for distributed transactions
- Dead letter queues and error handling"
```

### 8. DevOps Integration

#### Containerization
```bash
codex "Containerize my API for production deployment:
- Multi-stage Dockerfile optimization
- Docker Compose for local development
- Health check endpoints
- Non-root user configuration
- Resource limits and security scanning"
```

#### Kubernetes Deployment
```bash
codex "Create Kubernetes manifests for my API including:
- Deployment with rolling updates
- Service and ingress configuration
- ConfigMaps and Secrets management
- HPA (Horizontal Pod Autoscaler)
- Monitoring and logging setup"
```

#### CI/CD Pipeline
```bash
codex "Set up CI/CD pipeline for my API with:
- Automated testing on pull requests
- Code quality checks and security scanning
- Automated deployment to staging/production
- Database migration handling
- Rollback mechanisms and health monitoring"
```

### 9. Monitoring and Observability

#### Application Monitoring
```bash
codex "Add comprehensive monitoring to my API:
- Health check endpoints (/health, /ready)
- Prometheus metrics collection
- Application performance monitoring
- Error tracking and alerting
- Custom business metrics"
```

#### Logging Strategy
```bash
codex "Implement structured logging for my API:
- Structured JSON logging
- Correlation IDs for request tracing
- Log aggregation and analysis
- Security audit logging
- Performance metrics logging"
```

## Framework-Specific Enhancements

### FastAPI Specific
```bash
codex "Enhance my FastAPI application with:
- Async database operations with asyncpg
- Background tasks with Celery
- WebSocket support for real-time features
- Dependency injection for services
- Custom middleware for [specific needs]"
```

### Express.js Specific
```bash
codex "Optimize my Express.js API with:
- TypeScript strict mode configuration
- Custom middleware for [functionality]
- Error handling middleware
- Request validation with Joi/Yup
- Session management with Redis"
```

### Django Specific
```bash
codex "Enhance my Django REST API with:
- Custom permission classes
- DRF spectacular for OpenAPI docs
- Celery for background tasks
- Django signals for business logic
- Custom management commands"
```

## Usage Tips

### Effective Prompting
1. **Be Specific**: Include framework, database, and specific requirements
2. **Context Matters**: Reference existing code and architectural decisions
3. **Iterative Development**: Build features incrementally through conversation
4. **Security First**: Always mention security and validation requirements

### Project Context
1. **AGENTS.md**: Maintain project context between sessions
2. **Existing Patterns**: Reference established code patterns
3. **Architecture Decisions**: Document and reference design choices
4. **Performance Requirements**: Specify scalability and performance needs

### Code Quality
1. **Testing**: Always include testing requirements in prompts
2. **Documentation**: Request inline documentation and API specs
3. **Error Handling**: Specify comprehensive error handling needs
4. **Security**: Include security considerations in all prompts