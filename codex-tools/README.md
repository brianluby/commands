# 🤖 Codex CLI Tools
*Production-Ready Natural Language Development Commands*

## Overview
This collection adapts 52 production-ready Claude Code commands for OpenAI Codex CLI methodology. Instead of slash commands, these tools use natural language prompts and AGENTS.md project context for conversational development.

## What is Codex CLI?
[OpenAI Codex CLI](https://github.com/openai/codex) is a lightweight coding agent that runs locally in your terminal. It uses natural language to understand your development needs and directly modifies your codebase through conversation.

## Key Methodology Differences

### Claude Code (Original)
```bash
/api-scaffold "FastAPI user management with JWT auth"
# → Executes fixed template with subagent orchestration
# → Generates static output based on arguments
```

### Codex CLI (Adapted)
```bash
codex "Create a FastAPI user management API with JWT authentication"
# → Analyzes existing project context from AGENTS.md
# → Engages in conversation to understand requirements
# → Iteratively builds and refines implementation
# → Directly modifies local files with your approval
```

## Tool Categories

### 🔧 **Core Development Tools** (Phase 1)
High-value commands adapted for conversational development:

| Original Command | Codex CLI Prompt | Purpose |
|-----------------|------------------|---------|
| `/api-scaffold` | `"Create a [framework] API for [feature]"` | API endpoint generation |
| `/security-scan` | `"Analyze this code for security vulnerabilities"` | Security analysis |
| `/test-harness` | `"Create comprehensive tests for [component]"` | Test generation |
| `/docker-optimize` | `"Optimize this Dockerfile for production"` | Container optimization |
| `/k8s-manifest` | `"Generate K8s manifests for this app"` | Kubernetes deployment |

### 📋 **AGENTS.md Templates** (Phase 2)
Project context and memory systems:
- Framework-specific project templates
- Architecture decision records
- Code convention documentation
- Development workflow patterns

### 🔄 **Multi-Turn Workflows** (Phase 3)
Complex development patterns:
- Feature development conversations
- Code review and improvement cycles
- Deployment pipeline creation
- Performance optimization workflows

## Quick Start

### 1. Install Codex CLI
```bash
npm install -g @openai/codex
# or
brew install codex
```

### 2. Initialize Your Project
```bash
# In your project directory
codex "Help me set up AGENTS.md for this project"
```

### 3. Start Building
```bash
# Natural language development
codex "I need to add user authentication to my FastAPI application"

# Code analysis and improvement
codex "Review this authentication code and suggest security improvements"

# Testing and validation
codex "Create comprehensive tests for the user registration flow"
```

## Directory Structure

```
codex-tools/
├── prompts/                    # Natural language prompt patterns
│   ├── api-development.md      # API creation prompts
│   ├── security-analysis.md    # Security scanning prompts
│   ├── testing-strategies.md   # Test generation prompts
│   └── deployment.md          # DevOps and deployment prompts
│
├── agents-templates/           # AGENTS.md templates
│   ├── fastapi-project.md     # FastAPI project template
│   ├── react-app.md           # React application template
│   ├── microservices.md       # Microservices architecture
│   └── full-stack.md          # Full-stack application
│
└── workflows/                 # Multi-turn conversation patterns
    ├── feature-development.md  # End-to-end feature creation
    ├── security-hardening.md  # Security improvement workflow
    ├── performance-tuning.md  # Performance optimization
    └── deployment-pipeline.md # CI/CD setup workflow
```

## Advantages of Codex CLI Approach

### 🎯 **Context-Aware Development**
- **Project Memory**: AGENTS.md maintains context between sessions
- **Codebase Understanding**: Analyzes existing code before making changes
- **Iterative Refinement**: Builds features through conversation, not templates

### 🔄 **Interactive Development**
- **Multi-Turn Conversations**: Complex features built step-by-step
- **Real-Time Feedback**: Immediate clarification and adjustment
- **Approval Gates**: You control what changes are applied

### 🏗️ **Local Integration**
- **Direct File Modification**: Changes your actual codebase
- **Git Integration**: Tracks changes with proper version control
- **Development Environment**: Works with your existing setup

### 📚 **Learning and Adaptation**
- **Pattern Recognition**: Learns your coding style and preferences
- **Best Practices**: Incorporates security and performance considerations
- **Knowledge Transfer**: Explains decisions and teaches concepts

## Migration from Claude Code

### For Claude Code Users
If you're familiar with Claude Code commands, here's how to translate:

```bash
# Claude Code
/api-scaffold "user management API with authentication"

# Codex CLI equivalent
codex "Create a user management API with authentication for my FastAPI project"
```

### Key Differences
1. **No slash syntax** - Use natural language
2. **Context awareness** - Codex analyzes your existing project
3. **Conversational** - Engage in dialogue to refine requirements
4. **Direct modification** - Changes your actual files (with approval)

## Example Usage Patterns

### API Development
```bash
codex "I need a REST API for a blog application with posts, comments, and user management"
# → Analyzes project structure
# → Suggests appropriate framework
# → Creates endpoints iteratively
# → Adds authentication and validation
# → Generates tests and documentation
```

### Security Analysis
```bash
codex "Analyze my authentication system for security vulnerabilities and suggest improvements"
# → Reviews authentication code
# → Identifies potential issues
# → Suggests specific improvements
# → Implements fixes with your approval
# → Adds security tests
```

### Testing Strategy
```bash
codex "Create a comprehensive testing strategy for my e-commerce API"
# → Analyzes API endpoints
# → Suggests test categories (unit, integration, e2e)
# → Creates test files and fixtures
# → Sets up testing infrastructure
# → Adds CI/CD integration
```

## Integration with Development Workflow

### Version Control
```bash
# Before major changes
git checkout -b feature/user-auth

# Use Codex for development
codex "Add JWT-based authentication to my FastAPI app"

# Review and commit changes
git add . && git commit -m "Add JWT authentication system"
```

### Code Review
```bash
# Before submitting PR
codex "Review this code for best practices and potential issues"

# Performance optimization
codex "Analyze this code for performance bottlenecks and suggest optimizations"
```

### Deployment
```bash
# Containerization
codex "Create a production-ready Dockerfile for this FastAPI application"

# Kubernetes deployment
codex "Generate Kubernetes manifests with proper resource limits and health checks"
```

This approach transforms development from template-based generation to intelligent, conversational programming that adapts to your specific project needs and coding style.