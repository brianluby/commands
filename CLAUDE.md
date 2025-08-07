# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a collection of production-ready slash commands for Claude Code that accelerate development through intelligent automation. The repository contains 52 commands organized as workflows (multi-subagent orchestration) and tools (single-purpose utilities).

## Key Commands

### Installation and Setup
```bash
# Clone into Claude Code directory
cd ~/.claude
git clone https://github.com/wshobson/commands.git
git clone https://github.com/wshobson/agents.git  # Required for subagent orchestration
```

### Command Structure
- **Workflows** (`workflows/`): Multi-subagent orchestration for complex tasks
- **Tools** (`tools/`): Single-purpose commands for specific operations
- Commands are markdown files where the filename becomes the slash command

## Architecture and Usage Patterns

### Command Types

#### 🤖 Workflows (14 commands)
Use workflows for complex, multi-domain tasks requiring coordination:
- **feature-development**: Orchestrates backend, frontend, testing, and deployment subagents
- **full-review**: Multiple review subagents provide comprehensive code analysis
- **smart-fix**: Analyzes issues and delegates to appropriate specialist subagents
- **legacy-modernize**: Modernizes codebases using specialized subagents
- **security-hardening**: Security-first implementation with specialized subagents

#### 🔧 Tools (38 commands)
Use tools for focused, single-domain tasks:
- **api-scaffold**: Generate production-ready API endpoints with complete implementation
- **security-scan**: Comprehensive security scanning with automated remediation
- **test-harness**: Create comprehensive test suites with framework detection
- **docker-optimize**: Advanced container optimization strategies
- **k8s-manifest**: Production-grade Kubernetes deployments

### Command Integration Patterns

#### Sequential Execution
```bash
# Build → Test → Secure → Deploy pipeline
/api-scaffold user management API
/test-harness comprehensive test suite for user API  
/security-scan check user API for vulnerabilities
/k8s-manifest deploy user API to production
```

#### Multi-Agent Coordination
```bash
# Complex feature implementation
/feature-development Add real-time chat feature with WebSocket support
# Uses backend-architect → frontend-developer → test-automator → deployment-engineer
```

#### Problem-Solving Workflows
```bash
# Intelligent issue resolution
/smart-fix Fix performance degradation in API response times
# Analyzes issue and routes to appropriate specialist (performance-engineer, database-optimizer, etc.)
```

### Task Delegation with Task Tool

Workflows use explicit Task tool invocations to delegate to specialized subagents:
- `subagent_type="backend-architect"` for API design
- `subagent_type="frontend-developer"` for UI components  
- `subagent_type="test-automator"` for comprehensive testing
- `subagent_type="deployment-engineer"` for production deployment
- `subagent_type="debugger"` for code error analysis
- `subagent_type="performance-engineer"` for optimization
- `subagent_type="devops-troubleshooter"` for infrastructure issues

## Development Workflow Recommendations

### For New Features
1. Use `/feature-development` for complete feature implementation
2. Follow up with `/security-scan` for security validation
3. Use `/docker-optimize` for containerization
4. Deploy with `/k8s-manifest` for Kubernetes

### For Bug Fixes
1. Use `/smart-fix` for intelligent issue analysis and routing
2. Follow up with `/test-harness` to prevent regression
3. Use `/error-analysis` for root cause investigation

### For Code Quality
1. Use `/refactor-clean` for maintainability improvements
2. Use `/tech-debt` for technical debt analysis
3. Use `/code-explain` for complex code documentation

### For DevOps Tasks
1. Use `/docker-optimize` for container optimization
2. Use `/k8s-manifest` for Kubernetes deployments
3. Use `/monitor-setup` for observability
4. Use `/workflow-automate` for CI/CD pipeline creation

## Important Notes

- Commands work together seamlessly - outputs from one command can be inputs to another
- Workflows coordinate multiple subagents automatically using the Task tool
- All commands focus on production-ready implementations with security and best practices
- Framework auto-detection ensures commands work with existing tech stacks
- Commands include comprehensive examples and integration patterns

## Command Selection Guidelines

### Use Workflows When:
- Problem-solving with unknown solutions
- Complex tasks spanning multiple domains
- Need multiple perspectives from specialist subagents
- Want coordinated implementation across stack layers

### Use Tools When:
- Specific expertise needed in one domain
- Precise control over implementation details
- Building on existing work or enhancing previous outputs
- Focused, single-purpose operations

The repository structure follows a clear separation between orchestration logic (workflows) and specialized implementations (tools), enabling both high-level automation and precise control over specific development tasks.