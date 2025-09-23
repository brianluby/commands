# Codex CLI Tools Adaptation TODO

## Overview
This repository contains 52 production-ready Claude Code commands that need adaptation for OpenAI Codex CLI methodology. The new OpenAI Codex CLI is a lightweight coding agent that runs locally and uses natural language prompts to perform coding tasks.

## Key Differences to Address

### Command Interface
- **Current**: Claude Code slash commands (`/api-scaffold`) with `$ARGUMENTS` in `~/.claude/` directory
- **Needed**: Codex CLI natural language prompts and AGENTS.md integration patterns:
  - Terminal-based conversational interface: `codex "create a FastAPI user management API"`
  - AGENTS.md files for project context and memory
  - Multi-turn conversations with iterative development
  - Local file system integration with direct code modification

### Execution Environment
- **Current**: Unified Claude Code environment with subagent orchestration
- **Needed**: Local terminal-based agent approach:
  - **CLI Integration**: Direct terminal commands with natural language
  - **Project Context**: AGENTS.md files for maintaining project memory
  - **File Operations**: Direct reading and writing to local filesystem
  - **Iterative Development**: Multi-turn conversations for complex tasks

### Agent Architecture
- **Current**: Multi-agent workflows with specialized subagents (`backend-architect`, `security-expert`)
- **Needed**: Single conversational agent with specialized prompting:
  - Context-aware natural language instructions
  - AGENTS.md project memory and context persistence
  - Iterative task breakdown through conversation
  - Local filesystem operations and direct code modification

## Adaptation Strategy

### Phase 1: Core CLI Commands (High-Value Commands)
Transform Claude Code commands into Codex CLI natural language prompts and AGENTS.md patterns:
1. **api-scaffold** → "Create a [framework] API for [feature] with [requirements]"
2. **security-scan** → "Analyze this codebase for security vulnerabilities and suggest fixes"
3. **docker-optimize** → "Optimize this Dockerfile for production deployment"
4. **test-harness** → "Create comprehensive tests for this [component/API/feature]"
5. **k8s-manifest** → "Generate Kubernetes manifests for this application"

### Phase 2: AGENTS.md Integration Patterns
Develop project context and memory systems:
- AGENTS.md templates for different project types
- Context persistence between Codex CLI sessions
- Project-specific instructions and conventions
- Code style and architectural pattern memory

### Phase 3: Advanced Workflows
Create complex multi-step development patterns:
- Multi-turn conversations for feature development
- Iterative code review and improvement cycles
- Integration with local development workflows
- Automated testing and deployment pipeline integration

## High-Value Commands to Prioritize

### Tier 1: Direct Code Generation
1. **api-scaffold** - REST API endpoint generation
2. **test-harness** - Test suite generation
3. **docker-optimize** - Dockerfile and container optimization
4. **k8s-manifest** - Kubernetes deployment generation
5. **security-scan** - Security analysis and remediation

### Tier 2: Analysis and Enhancement
6. **refactor-clean** - Code refactoring assistance
7. **performance-optimization** - Performance analysis and improvements
8. **error-analysis** - Bug detection and fixing
9. **code-explain** - Code documentation and explanation
10. **deps-upgrade** - Dependency analysis and updates

### Tier 3: Workflow Integration
11. **deploy-checklist** - Deployment automation
12. **monitor-setup** - Observability and monitoring
13. **workflow-automate** - CI/CD pipeline generation
14. **tech-debt** - Technical debt analysis
15. **onboard** - Developer onboarding automation

## Codex CLI Implementation Patterns

### 1. Natural Language Commands
```bash
# Direct CLI invocation with natural language
codex "Create a FastAPI user management API with JWT authentication and PostgreSQL"

# Multi-step feature development
codex "Add secure password reset functionality to the existing user API"

# Code analysis and improvement
codex "Review this authentication code for security vulnerabilities and suggest improvements"

# Testing and validation
codex "Generate comprehensive tests for the user registration endpoint"
```

### 2. AGENTS.md Project Context
```markdown
# AGENTS.md - Project Memory and Context

## Project Overview
FastAPI e-commerce application with user management, product catalog, and order processing.

## Architecture Decisions
- Framework: FastAPI with async/await patterns
- Database: PostgreSQL with SQLAlchemy ORM
- Authentication: JWT tokens with refresh mechanism
- Testing: pytest with async test support
- Deployment: Docker containers on Kubernetes

## Code Conventions
- Use Pydantic models for all request/response schemas
- Implement proper error handling with custom HTTP exceptions
- Follow REST API conventions with proper HTTP status codes
- Include comprehensive docstrings and type hints
- Use dependency injection for database sessions and auth

## Current Implementation Status
- [x] User registration and authentication
- [x] Product catalog with categories
- [ ] Shopping cart functionality (in progress)
- [ ] Order processing and payment integration
- [ ] Admin dashboard and analytics
```

### 3. Interactive Development Sessions
```bash
# Start a development session
codex "I need to add shopping cart functionality to my e-commerce API"

# Codex analyzes AGENTS.md and existing code, then responds:
# "I can see you have a FastAPI e-commerce app with users and products. 
#  For the shopping cart, I'll create CartItem and Cart models that integrate 
#  with your existing User and Product models. Should I also add cart persistence 
#  and session management?"

# Continue the conversation
codex "Yes, and include cart expiration and merge functionality for logged-in users"

# Codex iteratively builds the feature through conversation
```

### 4. Project-Specific Patterns
```bash
# Framework-specific commands
codex "Add a new Django model for blog posts with proper relationships"

# Architecture-specific requests  
codex "Create a microservice for order processing that communicates with the user service"

# DevOps and deployment
codex "Generate Kubernetes manifests for this FastAPI application with proper resource limits"

# Security and compliance
codex "Audit this authentication system for OWASP Top 10 vulnerabilities"
```

## Integration Patterns

### GitHub Copilot Chat Prompts
```
/api Generate a FastAPI endpoint for user registration with email validation
/security Review this authentication code for vulnerabilities
/test Create comprehensive tests for this API endpoint
/docker Optimize this Dockerfile for production deployment
```

### API-Driven Workflows
```python
# Automated code generation pipeline
def generate_full_api_stack(requirements: dict):
    tools = [
        CodexAPIGenerator(),
        CodexSecurityAnalyzer(), 
        CodexTestGenerator(),
        CodexDockerOptimizer()
    ]
    
    for tool in tools:
        tool.process(requirements)
```

### IDE Integration Points
- **VS Code**: Custom snippets and commands
- **JetBrains**: Live templates and intentions
- **Vim/Neovim**: Custom functions and key bindings
- **Sublime Text**: Custom packages and commands

## Modern Codex Evolution

### Current State (2024)
- **OpenAI Codex models**: Deprecated (March 2023)
- **GitHub Copilot**: Primary consumer implementation
- **OpenAI API**: GPT-3.5/4 with code generation capabilities
- **Modern Models**: Code-specific fine-tuned models

### Integration Opportunities
- **GitHub Copilot Extensions**: Custom agent development
- **OpenAI Function Calling**: Structured code generation
- **Fine-tuned Models**: Domain-specific code generation
- **Multi-modal Models**: Code generation from designs/specs

## Success Metrics

### Code Generation Quality
- **Syntax Accuracy**: Generated code compiles/runs without errors
- **Best Practices**: Follows framework conventions and security patterns
- **Completeness**: Includes necessary imports, error handling, documentation
- **Maintainability**: Generated code is readable and well-structured

### Developer Productivity
- **Time Savings**: Reduced time from requirement to working code
- **Learning Curve**: Easy adoption of new frameworks and patterns
- **Error Reduction**: Fewer bugs in generated vs hand-written code
- **Consistency**: Uniform code style and patterns across projects

### Integration Success
- **IDE Adoption**: Seamless integration with development environments
- **Workflow Integration**: Fits into existing development processes
- **Team Collaboration**: Facilitates knowledge sharing and onboarding
- **Maintenance**: Easy to update and extend tool capabilities

## Technical Changes Needed

### From Claude Code to Codex CLI
- **Replace** Slash commands (`/api-scaffold`) → **Natural language prompts** ("Create a FastAPI API for user management")
- **Replace** `$ARGUMENTS` placeholders → **Conversational context** and **iterative clarification**
- **Replace** Subagent orchestration → **Multi-turn conversations** with single agent
- **Replace** Fixed command templates → **AGENTS.md project context** and **adaptive prompting**
- **Replace** Directory-based commands → **Local filesystem integration** with direct code modification

### Codex CLI Integration Requirements
- **ChatGPT/OpenAI account** with appropriate plan (Plus, Pro, Team, Enterprise)
- **Local terminal access** for CLI-based interactions
- **Project-specific AGENTS.md** files for context persistence
- **Git integration** for version control and change tracking
- **Local development environment** setup and configuration

### Methodology Alignment
- **Conversational Development**: Multi-turn interactions vs single-command execution
- **Project Memory**: AGENTS.md context vs stateless command execution  
- **Local File Operations**: Direct filesystem modification vs template generation
- **Iterative Refinement**: Progressive improvement through conversation vs one-shot results

This adaptation transforms Claude Code's template-based command system into Codex CLI's conversational agent methodology while maintaining the production-ready quality and comprehensive coverage of the original implementations.