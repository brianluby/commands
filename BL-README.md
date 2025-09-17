<<<<<<< HEAD

<!-- Language selector commented out for fork
<div align="right">
  <details>
    <summary >🌐 Language</summary>
    <div>
      <div align="center">
        <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=en">English</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=zh-CN">简体中文</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=zh-TW">繁體中文</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=ja">日本語</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=ko">한국어</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=hi">हिन्दी</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=th">ไทย</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=fr">Français</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=de">Deutsch</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=es">Español</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=it">Italiano</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=ru">Русский</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=pt">Português</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=nl">Nederlands</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=pl">Polski</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=ar">العربية</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=fa">فارسی</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=tr">Türkçe</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=vi">Tiếng Việt</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=id">Bahasa Indonesia</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=commands&lang=as">অসমীয়া</
      </div>
    </div>
  </details>
</div>
-->

=======
>>>>>>> upstream/main
# Claude Code Slash Commands

A comprehensive collection of production-ready slash commands for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that provides intelligent automation and multi-agent orchestration capabilities for modern software development.

<<<<<<< HEAD
**62 commands** organized as:
- **🤖 Workflows**: Multi-subagent orchestration for complex tasks
- **🔧 Tools**: Single-purpose utilities for specific operations

### 🌟 About This Fork

This repository is a fork of the excellent [original Claude Code Commands](https://github.com/wshobson/commands) created by [Seth Hobson](https://github.com/wshobson). We are deeply grateful for the solid foundation and comprehensive command set that Seth has built for the Claude Code community.

This fork includes additional customizations and improvements:
- Enhanced Rust development tools (8 new commands)
- Quality assurance infrastructure (testing, versioning, pre-commit hooks)
- Additional development workflows tailored for our team

We maintain compatibility with the upstream repository and regularly sync to incorporate new features.

### 🤝 Requires Claude Code Subagents
=======
## Overview

This repository provides **56 production-ready slash commands** (15 workflows, 41 tools) that extend Claude Code's capabilities through:
>>>>>>> upstream/main

- **Workflows**: Multi-agent orchestration systems that coordinate complex, multi-step operations across different domains
- **Tools**: Specialized single-purpose utilities for focused development tasks

## System Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and configured
- [Claude Code Subagents](https://github.com/wshobson/agents) collection for workflow orchestration capabilities
- Git for repository management

## Installation

```bash
# Navigate to Claude configuration directory
cd ~/.claude
<<<<<<< HEAD
git clone https://github.com/brianluby/commands.git
git clone https://github.com/wshobson/agents.git  # Required for subagent orchestration
```

> **Note:** If you've already cloned the original repository, you can add this fork as a remote:
> ```bash
> cd ~/.claude/commands
> git remote add fork https://github.com/brianluby/commands.git
> git fetch fork
> git checkout -b custom-features fork/main
> ```

## Available Commands
=======

# Clone the commands repository
git clone https://github.com/wshobson/commands.git

# Clone the agents repository (required for workflow execution)
git clone https://github.com/wshobson/agents.git
```

## Command Invocation
>>>>>>> upstream/main

Commands are organized in `tools/` and `workflows/` directories and invoked using directory prefixes:

```bash
# Workflow invocation
/workflows:feature-development implement OAuth2 authentication

# Tool invocation
/tools:security-scan perform vulnerability assessment

# Multiple argument example
/tools:api-scaffold create user management endpoints with RBAC
```

### Alternative Setup (No Prefixes)

<<<<<<< HEAD
## 🤖 Workflows

Multi-subagent orchestration for complex tasks:

### Feature Development
- **[feature-development](workflows/feature-development.md)** - Backend, frontend, testing, and deployment subagents build complete features
- **[full-review](workflows/full-review.md)** - Multiple review subagents provide comprehensive code analysis
- **[smart-fix](workflows/smart-fix.md)** - Analyzes issues and delegates to appropriate specialist subagents

### Development Processes
- **[git-workflow](workflows/git-workflow.md)** - Implements effective Git workflows with branching strategies and PR templates
- **[improve-agent](workflows/improve-agent.md)** - Enhances subagent performance through prompt optimization
- **[legacy-modernize](workflows/legacy-modernize.md)** - Modernizes legacy codebases using specialized subagents
- **[ml-pipeline](workflows/ml-pipeline.md)** - Creates ML pipelines with data and ML engineering subagents
- **[multi-platform](workflows/multi-platform.md)** - Builds cross-platform apps with coordinated subagents
- **[workflow-automate](workflows/workflow-automate.md)** - Automates CI/CD, monitoring, and deployment workflows

### Subagent-Orchestrated Workflows
- **[full-stack-feature](workflows/full-stack-feature.md)** - Multi-platform features with backend, frontend, and mobile subagents
- **[security-hardening](workflows/security-hardening.md)** - Security-first implementation with specialized subagents
- **[data-driven-feature](workflows/data-driven-feature.md)** - ML-powered features with data science subagents
- **[performance-optimization](workflows/performance-optimization.md)** - End-to-end optimization with performance subagents
- **[incident-response](workflows/incident-response.md)** - Production incident resolution with ops subagents

## 🔧 Tools (Single-Purpose Commands)

### AI & Machine Learning
- **[ai-assistant](tools/ai-assistant.md)** - Build production-ready AI assistants and chatbots
- **[ai-review](tools/ai-review.md)** - Specialized review for AI/ML codebases
- **[langchain-agent](tools/langchain-agent.md)** - Create LangChain/LangGraph agents with modern patterns
- **[ml-pipeline](tools/ml-pipeline.md)** - Create end-to-end ML pipelines with MLOps
- **[prompt-optimize](tools/prompt-optimize.md)** - Optimize AI prompts for performance and quality

### Architecture & Code Quality
- **[code-explain](tools/code-explain.md)** - Generate detailed explanations of complex code
- **[code-migrate](tools/code-migrate.md)** - Migrate code between languages, frameworks, or versions
- **[refactor-clean](tools/refactor-clean.md)** - Refactor code for maintainability and performance
- **[tech-debt](tools/tech-debt.md)** - Analyze and prioritize technical debt

### Data & Database
- **[data-pipeline](tools/data-pipeline.md)** - Design scalable data pipeline architectures
- **[data-validation](tools/data-validation.md)** - Implement comprehensive data validation systems
- **[db-migrate](tools/db-migrate.md)** - Advanced database migration strategies

### DevOps & Infrastructure
- **[deploy-checklist](tools/deploy-checklist.md)** - Generate deployment configurations and checklists
- **[docker-optimize](tools/docker-optimize.md)** - Advanced container optimization strategies
- **[k8s-manifest](tools/k8s-manifest.md)** - Production-grade Kubernetes deployments
- **[monitor-setup](tools/monitor-setup.md)** - Set up comprehensive monitoring and observability
- **[slo-implement](tools/slo-implement.md)** - Implement Service Level Objectives (SLOs)
- **[workflow-automate](tools/workflow-automate.md)** - Automate development and operational workflows

### Development & Testing
- **[api-mock](tools/api-mock.md)** - Create realistic API mocks for development and testing
- **[api-scaffold](tools/api-scaffold.md)** - Generate production-ready API endpoints with complete implementation stack
- **[test-harness](tools/test-harness.md)** - Create comprehensive test suites with framework detection

### Security & Compliance
- **[accessibility-audit](tools/accessibility-audit.md)** - Comprehensive accessibility testing and fixes
- **[compliance-check](tools/compliance-check.md)** - Ensure regulatory compliance (GDPR, HIPAA, SOC2)
- **[security-scan](tools/security-scan.md)** - Comprehensive security scanning with automated remediation

### Debugging & Analysis
- **[debug-trace](tools/debug-trace.md)** - Advanced debugging and tracing strategies
- **[error-analysis](tools/error-analysis.md)** - Deep error pattern analysis and resolution strategies
- **[error-trace](tools/error-trace.md)** - Trace and diagnose production errors
- **[issue](tools/issue.md)** - Create well-structured GitHub/GitLab issues

### Dependencies & Configuration
- **[config-validate](tools/config-validate.md)** - Validate and manage application configuration
- **[deps-audit](tools/deps-audit.md)** - Audit dependencies for security and licensing
- **[deps-upgrade](tools/deps-upgrade.md)** - Safely upgrade project dependencies

### Documentation & Collaboration
- **[doc-generate](tools/doc-generate.md)** - Generate comprehensive documentation
- **[git-workflow](tools/git-workflow.md)** - Implement effective Git workflows
- **[pr-enhance](tools/pr-enhance.md)** - Enhance pull requests with quality checks

### Cost Optimization
- **[cost-optimize](tools/cost-optimize.md)** - Optimize cloud and infrastructure costs

### Onboarding & Setup
- **[onboard](tools/onboard.md)** - Set up development environments for new team members

### Rust Development
- **[rust-analyzer](tools/rust-analyzer.md)** - Deep static analysis and refactoring for Rust code
- **[rust-bench](tools/rust-bench.md)** - Performance benchmarking with Criterion and flamegraphs
- **[rust-fuzz](tools/rust-fuzz.md)** - Fuzzing infrastructure with cargo-fuzz and AFL++
- **[rust-io-optimize](tools/rust-io-optimize.md)** - Platform-specific I/O optimizations
- **[rust-error-design](tools/rust-error-design.md)** - Design robust error handling systems
- **[rust-async](tools/rust-async.md)** - Async runtime optimization with Tokio
- **[rust-cli](tools/rust-cli.md)** - CLI application framework with Clap
- **[rust-unsafe-audit](tools/rust-unsafe-audit.md)** - Comprehensive unsafe code auditing

### Subagent Tools
- **[multi-agent-review](tools/multi-agent-review.md)** - Multi-perspective code review with specialized subagents
- **[smart-debug](tools/smart-debug.md)** - Deep debugging with debugger and performance subagents
- **[multi-agent-optimize](tools/multi-agent-optimize.md)** - Full-stack optimization with multiple subagents
- **[context-save](tools/context-save.md)** - Save project context using context-manager subagent
- **[context-restore](tools/context-restore.md)** - Restore saved context for continuity

## Features

- Production-ready implementations
- Framework auto-detection
- Security best practices
- Built-in monitoring and testing
- Commands work together seamlessly

## Command Count

**Total: 62 production-ready slash commands** organized into:

### 🤖 Workflows (14 commands)

- Feature Development & Review (3 commands) 
- Development Process Automation (6 commands)
- Subagent-Orchestrated Workflows (5 commands)

### 🔧 Tools (48 commands)

- AI & Machine Learning (5 commands)
- Architecture & Code Quality (4 commands)
- Data & Database (3 commands)
- DevOps & Infrastructure (6 commands)
- Development & Testing (3 commands)
- Security & Compliance (3 commands)
- Debugging & Analysis (4 commands)
- Dependencies & Configuration (3 commands)
- Documentation & Collaboration (1 command)
- Onboarding & Setup (1 command)
- Rust Development (8 commands)
- Subagent-Specific Tools (5 commands)

## Usage Examples

### 🤖 Workflow Examples
=======
To invoke commands without directory prefixes, copy files to the root directory:
>>>>>>> upstream/main

```bash
cp tools/*.md .
cp workflows/*.md .

# Then invoke directly
/api-scaffold create REST endpoints
/feature-development implement payment system
```

## Command Architecture

### Workflows (15 commands)

Workflows implement multi-agent orchestration patterns for complex, cross-domain tasks. Each workflow analyzes requirements, delegates to specialized agents, and coordinates execution across multiple subsystems.

#### Core Development Workflows

| Command | Purpose | Agent Coordination |
|---------|---------|-------------------|
| `feature-development` | End-to-end feature implementation | Backend, frontend, testing, deployment |
| `full-review` | Multi-perspective code analysis | Architecture, security, performance, quality |
| `smart-fix` | Intelligent problem resolution | Dynamic agent selection based on issue type |
| `tdd-cycle` | Test-driven development orchestration | Test writer, implementer, refactoring specialist |

#### Process Automation Workflows

| Command | Purpose | Scope |
|---------|---------|-------|
| `git-workflow` | Version control process automation | Branching strategies, commit standards, PR templates |
| `improve-agent` | Agent optimization | Prompt engineering, performance tuning |
| `legacy-modernize` | Codebase modernization | Architecture migration, dependency updates, pattern refactoring |
| `ml-pipeline` | Machine learning pipeline construction | Data engineering, model training, deployment |
| `multi-platform` | Cross-platform development | Web, mobile, desktop coordination |
| `workflow-automate` | CI/CD pipeline automation | Build, test, deploy, monitor |

#### Advanced Orchestration Workflows

| Command | Primary Focus | Specialized Agents |
|---------|---------------|-------------------|
| `full-stack-feature` | Multi-tier implementation | Backend API, frontend UI, mobile, database |
| `security-hardening` | Security-first development | Threat modeling, vulnerability assessment, remediation |
| `data-driven-feature` | ML-powered functionality | Data science, feature engineering, model deployment |
| `performance-optimization` | System-wide optimization | Profiling, caching, query optimization, load testing |
| `incident-response` | Production issue resolution | Diagnostics, root cause analysis, hotfix deployment |

### Tools (41 commands)

Tools provide focused, single-purpose utilities for specific development operations. Each tool is optimized for its domain with production-ready implementations.

#### AI and Machine Learning (5 tools)

| Command | Functionality | Key Features |
|---------|--------------|--------------|
| `ai-assistant` | AI assistant implementation | LLM integration, conversation management, context handling |
| `ai-review` | ML code review | Model architecture validation, training pipeline review |
| `langchain-agent` | LangChain agent creation | RAG patterns, tool integration, memory management |
| `ml-pipeline` | ML pipeline construction | Data processing, training, evaluation, deployment |
| `prompt-optimize` | Prompt engineering | Performance testing, cost optimization, quality metrics |

#### Architecture and Code Quality (4 tools)

| Command | Purpose | Capabilities |
|---------|---------|--------------|
| `code-explain` | Code documentation | AST analysis, complexity metrics, flow diagrams |
| `code-migrate` | Migration automation | Framework upgrades, language porting, API migrations |
| `refactor-clean` | Code improvement | Pattern detection, dead code removal, structure optimization |
| `tech-debt` | Debt assessment | Complexity analysis, risk scoring, remediation planning |

#### Data and Database (3 tools)

| Command | Focus Area | Technologies |
|---------|------------|--------------|
| `data-pipeline` | ETL/ELT architecture | Apache Spark, Airflow, dbt, streaming platforms |
| `data-validation` | Data quality | Schema validation, anomaly detection, constraint checking |
| `db-migrate` | Database migrations | Schema versioning, zero-downtime strategies, rollback plans |

#### DevOps and Infrastructure (6 tools)

| Command | Domain | Implementation |
|---------|--------|----------------|
| `deploy-checklist` | Deployment preparation | Pre-flight checks, rollback procedures, monitoring setup |
| `docker-optimize` | Container optimization | Multi-stage builds, layer caching, size reduction |
| `k8s-manifest` | Kubernetes configuration | Deployments, services, ingress, autoscaling, security policies |
| `monitor-setup` | Observability | Metrics, logging, tracing, alerting rules |
| `slo-implement` | SLO/SLI definition | Error budgets, monitoring, automated responses |
| `workflow-automate` | Pipeline automation | CI/CD, GitOps, infrastructure as code |

#### Testing and Development (6 tools)

| Command | Testing Focus | Framework Support |
|---------|---------------|-------------------|
| `api-mock` | Mock generation | REST, GraphQL, gRPC, WebSocket |
| `api-scaffold` | Endpoint creation | CRUD operations, authentication, validation |
| `test-harness` | Test suite generation | Unit, integration, e2e, performance |
| `tdd-red` | Test-first development | Failing test creation, edge case coverage |
| `tdd-green` | Implementation | Minimal code to pass tests |
| `tdd-refactor` | Code improvement | Optimization while maintaining green tests |

#### Security and Compliance (3 tools)

| Command | Security Domain | Standards |
|---------|-----------------|-----------|
| `accessibility-audit` | WCAG compliance | ARIA, keyboard navigation, screen reader support |
| `compliance-check` | Regulatory compliance | GDPR, HIPAA, SOC2, PCI-DSS |
| `security-scan` | Vulnerability assessment | OWASP, CVE scanning, dependency audits |

#### Debugging and Analysis (4 tools)

| Command | Analysis Type | Output |
|---------|---------------|--------|
| `debug-trace` | Runtime analysis | Stack traces, memory profiles, execution paths |
| `error-analysis` | Error patterns | Root cause analysis, frequency analysis, impact assessment |
| `error-trace` | Production debugging | Log correlation, distributed tracing, error reproduction |
| `issue` | Issue tracking | Standardized templates, reproduction steps, acceptance criteria |

#### Dependency and Configuration Management (3 tools)

| Command | Management Area | Features |
|---------|-----------------|----------|
| `config-validate` | Configuration management | Schema validation, environment variables, secrets handling |
| `deps-audit` | Dependency analysis | Security vulnerabilities, license compliance, version conflicts |
| `deps-upgrade` | Version management | Breaking change detection, compatibility testing, rollback support |

#### Documentation and Collaboration (3 tools)

| Command | Documentation Type | Format |
|---------|-------------------|--------|
| `doc-generate` | API documentation | OpenAPI, JSDoc, TypeDoc, Sphinx |
| `pr-enhance` | Pull request optimization | Description generation, checklist creation, review suggestions |
| `standup-notes` | Status reporting | Progress tracking, blocker identification, next steps |

#### Operations and Context (4 tools)

| Command | Operational Focus | Use Case |
|---------|------------------|----------|
| `cost-optimize` | Resource optimization | Cloud spend analysis, right-sizing, reserved capacity |
| `onboard` | Environment setup | Development tools, access configuration, documentation |
| `context-save` | State persistence | Architecture decisions, configuration snapshots |
| `context-restore` | State recovery | Context reload, decision history, configuration restore |

## Usage Patterns

### Common Development Scenarios

#### Feature Implementation
```bash
# Complete feature with multi-agent orchestration
/workflows:feature-development OAuth2 authentication with JWT tokens

# API-first development
/tools:api-scaffold REST endpoints for user management with RBAC

# Test-driven approach
/workflows:tdd-cycle shopping cart with discount calculation logic
```

#### Debugging and Performance
```bash
# Intelligent issue resolution
/workflows:smart-fix high memory consumption in production workers

# Targeted error analysis
/tools:error-trace investigate Redis connection timeouts

# Performance optimization
/workflows:performance-optimization optimize database query performance
```

#### Security and Compliance
```bash
# Security assessment
/tools:security-scan OWASP Top 10 vulnerability scan

# Compliance verification
/tools:compliance-check GDPR data handling requirements

# Security hardening workflow
/workflows:security-hardening implement zero-trust architecture
```

### Test-Driven Development

#### Standard TDD Flow
```bash
# Complete TDD cycle with orchestration
/workflows:tdd-cycle payment processing with Stripe integration

# Manual TDD phases for granular control
/tools:tdd-red create failing tests for order validation
/tools:tdd-green implement minimal order validation logic
/tools:tdd-refactor optimize validation performance
```

### Command Composition Strategies

#### Sequential Execution Pattern
```bash
# Feature implementation pipeline
/workflows:feature-development real-time notifications with WebSockets
/tools:security-scan WebSocket implementation vulnerabilities
/workflows:performance-optimization WebSocket connection handling
/tools:deploy-checklist notification service deployment requirements
/tools:k8s-manifest WebSocket service with session affinity
```

#### Modernization Pipeline
```bash
# Legacy system upgrade
/workflows:legacy-modernize migrate monolith to microservices
/tools:deps-audit check dependency vulnerabilities
/tools:deps-upgrade update to latest stable versions
/tools:refactor-clean remove deprecated patterns
/tools:test-harness generate comprehensive test coverage
/tools:docker-optimize create optimized container images
/tools:k8s-manifest deploy with rolling update strategy
```

## Command Selection Guidelines

### Workflow vs Tool Decision Matrix

| Criteria | Use Workflows | Use Tools |
|----------|--------------|-----------|
| **Problem Complexity** | Multi-domain, cross-cutting concerns | Single domain, focused scope |
| **Solution Clarity** | Exploratory, undefined approach | Clear implementation path |
| **Agent Coordination** | Multiple specialists required | Single expertise sufficient |
| **Implementation Scope** | End-to-end features | Specific components |
| **Control Level** | Automated orchestration preferred | Manual control required |

### Workflow Selection Examples

| Requirement | Recommended Workflow | Rationale |
|-------------|---------------------|-----------|
| "Build complete authentication system" | `/workflows:feature-development` | Multi-tier implementation required |
| "Debug production performance issues" | `/workflows:smart-fix` | Unknown root cause, needs analysis |
| "Modernize legacy application" | `/workflows:legacy-modernize` | Complex refactoring across stack |
| "Implement ML-powered feature" | `/workflows:data-driven-feature` | Requires data science expertise |

### Tool Selection Examples

| Task | Recommended Tool | Output |
|------|-----------------|--------|
| "Generate Kubernetes configs" | `/tools:k8s-manifest` | YAML manifests with best practices |
| "Audit security vulnerabilities" | `/tools:security-scan` | Vulnerability report with fixes |
| "Create API documentation" | `/tools:doc-generate` | OpenAPI/Swagger specifications |
| "Optimize Docker images" | `/tools:docker-optimize` | Multi-stage Dockerfile |

## Execution Best Practices

### Context Optimization

1. **Technology Stack Specification**: Include framework versions, database systems, deployment targets
2. **Constraint Definition**: Specify performance requirements, security standards, compliance needs
3. **Integration Requirements**: Define external services, APIs, authentication methods
4. **Output Preferences**: Indicate coding standards, testing frameworks, documentation formats

### Command Chaining Strategies

1. **Progressive Enhancement**: Start with workflows for foundation, refine with tools
2. **Pipeline Construction**: Chain commands in logical sequence for complete solutions
3. **Iterative Refinement**: Use tool outputs as inputs for subsequent commands
4. **Parallel Execution**: Run independent tools simultaneously when possible

### Performance Considerations

- Workflows typically require 30-90 seconds for complete orchestration
- Tools execute in 5-30 seconds for focused operations
- Provide detailed requirements upfront to minimize iteration cycles
- Use saved context (`context-save`/`context-restore`) for multi-session projects

## Technical Architecture

### Command Structure

Each slash command is a markdown file with the following characteristics:

| Component | Description | Example |
|-----------|-------------|---------|
| **Filename** | Determines command name | `api-scaffold.md` → `/tools:api-scaffold` |
| **Content** | Execution instructions | Agent prompts and orchestration logic |
| **Variables** | `$ARGUMENTS` placeholder | Captures and processes user input |
| **Directory** | Command category | `tools/` for utilities, `workflows/` for orchestration |

### File Organization

```
~/.claude/commands/
├── workflows/          # Multi-agent orchestration commands
│   ├── feature-development.md
│   ├── smart-fix.md
│   └── ...
├── tools/             # Single-purpose utility commands
│   ├── api-scaffold.md
│   ├── security-scan.md
│   └── ...
└── README.md          # This documentation
```

## Development Guidelines

### Creating New Commands

#### Workflow Development

1. **File Creation**: Place in `workflows/` directory with descriptive naming
2. **Agent Orchestration**: Define delegation logic for multiple specialists
3. **Error Handling**: Include fallback strategies and error recovery
4. **Output Coordination**: Specify how agent outputs should be combined

#### Tool Development

1. **File Creation**: Place in `tools/` directory with single-purpose naming
2. **Implementation**: Provide complete, production-ready code generation
3. **Framework Detection**: Auto-detect and adapt to project stack
4. **Best Practices**: Include security, performance, and scalability considerations

### Naming Conventions

- Use lowercase with hyphens: `feature-name.md`
- Be descriptive but concise: `security-scan` not `scan`
- Indicate action clearly: `deps-upgrade` not `dependencies`
- Maintain consistency with existing commands

## Troubleshooting Guide

### Diagnostic Steps

| Issue | Cause | Resolution |
|-------|-------|------------|
| Command not recognized | File missing or misnamed | Verify file exists in correct directory |
| Slow execution | Normal workflow behavior | Workflows coordinate multiple agents (30-90s typical) |
| Incomplete output | Insufficient context | Provide technology stack and requirements |
| Integration failures | Path or configuration issues | Check file paths and dependencies |

### Performance Optimization

1. **Context Caching**: Use `context-save` for multi-session projects
2. **Batch Operations**: Combine related tasks in single workflow
3. **Tool Selection**: Use tools for known problems, workflows for exploration
4. **Requirement Clarity**: Detailed specifications reduce iteration cycles

## Featured Command Implementations

### Test-Driven Development Suite

| Command | Type | Capabilities |
|---------|------|--------------|
| `tdd-cycle` | Workflow | Complete red-green-refactor orchestration with test coverage analysis |
| `tdd-red` | Tool | Failing test generation with edge case coverage and mocking |
| `tdd-green` | Tool | Minimal implementation to achieve test passage |
| `tdd-refactor` | Tool | Code optimization while maintaining test integrity |

**Framework Support**: Jest, Mocha, PyTest, RSpec, JUnit, Go testing, Rust tests

### Security and Infrastructure

| Command | Specialization | Key Features |
|---------|---------------|--------------|
| `security-scan` | Vulnerability detection | SAST/DAST analysis, dependency scanning, secret detection |
| `docker-optimize` | Container optimization | Multi-stage builds, layer caching, size reduction (50-90% typical) |
| `k8s-manifest` | Kubernetes deployment | HPA, NetworkPolicy, PodSecurityPolicy, service mesh ready |
| `monitor-setup` | Observability | Prometheus metrics, Grafana dashboards, alert rules |

**Security Tools Integration**: Bandit, Safety, Trivy, Semgrep, Snyk, GitGuardian

### Data and Database Operations

| Command | Database Support | Migration Strategies |
|---------|-----------------|---------------------|
| `db-migrate` | PostgreSQL, MySQL, MongoDB, DynamoDB | Blue-green, expand-contract, versioned schemas |
| `data-pipeline` | Batch and streaming | Apache Spark, Kafka, Airflow, dbt integration |
| `data-validation` | Schema and quality | Great Expectations, Pandera, custom validators |

**Zero-Downtime Patterns**: Rolling migrations, feature flags, dual writes, backfill strategies

### Performance and Optimization

| Command | Analysis Type | Optimization Techniques |
|---------|--------------|------------------------|
| `performance-optimization` | Full-stack profiling | Query optimization, caching strategies, CDN configuration |
| `cost-optimize` | Cloud resource analysis | Right-sizing, spot instances, reserved capacity planning |
| `docker-optimize` | Container performance | Build cache optimization, minimal base images, layer reduction |

## Additional Resources

### Documentation

- [Claude Code Official Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Slash Commands Reference](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
- [Subagents Architecture](https://docs.anthropic.com/en/docs/claude-code/sub-agents)

### Source Repositories

- [Command Collection](https://github.com/wshobson/commands)
- [Agent Collection](https://github.com/wshobson/agents)
- [Claude Code Repository](https://github.com/anthropics/claude-code)

### Integration Examples

```bash
# Complete feature development pipeline
/workflows:feature-development user authentication system
/tools:security-scan authentication implementation
/tools:test-harness authentication test suite
/tools:docker-optimize authentication service
/tools:k8s-manifest authentication deployment
/tools:monitor-setup authentication metrics
```

## License

MIT License - See LICENSE file for complete terms.

## Support and Contribution

<<<<<<< HEAD
Comprehensive security scanning with automated remediation.

- **Multi-Tool Scanning**: Bandit, Safety, Trivy, Semgrep, ESLint Security, Snyk
- **Automated Fixes**: Common vulnerabilities auto-remediated
- **CI/CD Integration**: Security gates for GitHub Actions/GitLab CI
- **Container Scanning**: Image vulnerability analysis
- **Secret Detection**: GitLeaks and TruffleHog integration

#### [`/docker-optimize`](tools/docker-optimize.md)

Advanced container optimization strategies.

- **Smart Optimization**: Analyzes and suggests improvements
- **Multi-Stage Builds**: Framework-specific optimized Dockerfiles
- **Modern Tools**: BuildKit, Bun, UV for faster builds
- **Security Hardening**: Distroless images, non-root users
- **Cross-Command Integration**: Works with /api-scaffold outputs

#### [`/k8s-manifest`](tools/k8s-manifest.md)

Production-grade Kubernetes deployments.

- **Advanced Patterns**: Pod Security Standards, Network Policies, OPA
- **GitOps Ready**: FluxCD and ArgoCD configurations
- **Observability**: Prometheus ServiceMonitors, OpenTelemetry
- **Auto-Scaling**: HPA, VPA, and cluster autoscaler configs
- **Service Mesh**: Istio/Linkerd integration

### Frontend & Data

#### [`/db-migrate`](tools/db-migrate.md)

Advanced database migration strategies.

- **Multi-Database**: PostgreSQL, MySQL, MongoDB, DynamoDB
- **Zero-Downtime**: Blue-green deployments, rolling migrations
- **Event Sourcing**: Kafka/Kinesis integration for CDC
- **Cross-Platform**: Handles polyglot persistence
- **Monitoring**: Migration health checks and rollback

## Combining Workflows and Tools

The real power comes from combining workflows and tools for complete development cycles:

### Example: Building a New Feature

```bash
# 1. Use a workflow to implement the feature with multiple subagents
/feature-development Add real-time chat feature with WebSocket support

# 2. Use tools for specific enhancements
/test-harness Add integration tests for WebSocket connections
/security-scan Check for WebSocket vulnerabilities
/docker-optimize Optimize container for WebSocket connections

# 3. Use a workflow for comprehensive review
/full-review Review the entire chat feature implementation
```

### Example: Modernizing Legacy Code

```bash
# 1. Start with the modernization workflow
/legacy-modernize Migrate Express.js v4 app to modern architecture

# 2. Use specific tools for cleanup
/deps-upgrade Update all dependencies to latest versions
/refactor-clean Remove deprecated patterns and dead code
/test-harness Ensure 100% test coverage

# 3. Optimize and deploy
/docker-optimize Create multi-stage production build
/k8s-manifest Deploy with zero-downtime strategy
```

## Command Orchestration Patterns

Commands can be used individually or combined in powerful patterns:

### Sequential Execution
```bash
# Build → Test → Secure → Deploy pipeline
/api-scaffold user management API
/test-harness comprehensive test suite for user API  
/security-scan check user API for vulnerabilities
/k8s-manifest deploy user API to production
```

### Parallel Analysis
```bash
# Multiple perspectives on the same codebase
/multi-agent-review comprehensive architecture and code review
/security-scan audit security posture  
/performance-optimization identify and fix bottlenecks
# Then consolidate findings
```

### Iterative Refinement
```bash
# Start broad, then narrow focus
/feature-development implement payment processing
/security-scan focus on payment security
/compliance-check ensure PCI compliance
/test-harness add payment-specific tests
```

### Cross-Domain Integration
```bash
# Frontend + Backend + Infrastructure
/api-scaffold backend payment API
/multi-agent-optimize optimize payment flow performance
/docker-optimize containerize payment service
/monitor-setup payment metrics and alerts
```

## When to Use Workflows vs Tools

### 🔀 Workflows & Subagent Tools
- **Problem-solving**: Analyze and fix issues adaptively
- **Multiple perspectives**: Coordinate specialist subagents
- **Complex tasks**: Multi-step processes across domains
- **Unknown solutions**: Let subagents determine approach

### 🛠️ Specialized Tools
- **Infrastructure setup**: Configure environments
- **Code generation**: Create specific implementations
- **Analysis**: Generate reports without fixes
- **Domain tasks**: Highly specialized operations

**Examples:**
- "Implement user authentication system" → `/feature-development`
- "Fix performance issues across the stack" → `/smart-fix`
- "Modernize legacy monolith" → `/legacy-modernize`

### 🔧 Use Tools When:
- **Specific expertise needed** - Clear, focused task in one domain
- **Precise control desired** - Want to direct specific implementation details
- **Part of manual workflow** - Integrating into existing processes
- **Deep specialization required** - Need expert-level implementation
- **Building on existing work** - Enhancing or refining previous outputs

**Examples:**
- "Create Kubernetes manifests" → `/k8s-manifest`
- "Scan for security vulnerabilities" → `/security-scan`
- "Generate API documentation" → `/doc-generate`

## Command Format

Slash commands are simple markdown files where:
- The filename becomes the command name (e.g., `api-scaffold.md` → `/api-scaffold`)
- The file content is the prompt/instructions executed when invoked
- Use `$ARGUMENTS` placeholder for user input

## Best Practices

### Command Selection
- **Let Claude Code suggest automatically** - Analyzes context and selects optimal commands
- **Use workflows for complex tasks** - Subagents coordinate multi-domain implementations
- **Use tools for focused tasks** - Apply specific commands for targeted improvements

### Effective Usage
- **Provide comprehensive context** - Include tech stack, constraints, and requirements
- **Chain commands strategically** - Workflows → Tools → Refinements
- **Build on previous outputs** - Commands are designed to work together

## Our Fork Enhancements

This fork extends the original repository with:

### 🦀 Rust Development Suite (8 new tools)
- **rust-analyzer** - Deep static analysis and refactoring
- **rust-bench** - Performance benchmarking with Criterion
- **rust-fuzz** - Comprehensive fuzzing infrastructure
- **rust-io-optimize** - Platform-specific I/O optimizations
- **rust-error-design** - Error handling architecture
- **rust-async** - Async runtime optimization
- **rust-cli** - CLI application framework
- **rust-unsafe-audit** - Unsafe code security analysis

### 🔧 Development Infrastructure
- **Test Framework** - Command validation and quality checks
- **Version Manager** - Semantic versioning for commands
- **Pre-commit Hooks** - Automated quality enforcement
- **Error Standards** - Consistent error handling patterns
- **Development Guide** - Comprehensive contributor documentation

We maintain full compatibility with the upstream repository and regularly sync to incorporate new features.

## Contributing

### To This Fork
1. Create `.md` file in `workflows/` or `tools/`
2. Use lowercase-hyphen-names
3. Include `$ARGUMENTS` for user input
4. Test thoroughly with our development workflows
5. Submit PR with clear description of enhancements

### To Upstream
For general improvements that would benefit the broader community, consider contributing directly to the [original repository](https://github.com/wshobson/commands)

## Troubleshooting

**Command not found**: Check files are in `~/.claude/commands/`

**Workflows slow**: Normal - they coordinate multiple subagents

**Generic output**: Add more specific context about your tech stack

**Integration issues**: Verify file paths and command sequence

## Performance Tips

**Command Selection:**
- **Workflows**: Multi-subagent coordination for complex features
- **Tools**: Single-purpose operations for specific tasks
- **Simple edits**: Stay with main agent

**Optimization:**
- Start with tools for known problems
- Provide detailed requirements upfront
- Build on previous command outputs
- Let workflows complete before modifications

### Adding a New Workflow:
- Focus on subagent orchestration and delegation logic
- Specify which specialized subagents to use and in what order
- Define coordination patterns between subagents

### Adding a New Tool:
- Include complete, production-ready implementations
- Structure content with clear sections and actionable outputs
- Include examples, best practices, and integration points

## Learn More

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Slash Commands Documentation](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
- [Subagents Documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)
- [Claude Code Subagents Collection](https://github.com/wshobson/agents) - Specialized subagents used by these commands

## Credits

This collection builds upon the fantastic work by [Seth Hobson](https://github.com/wshobson) in creating a comprehensive set of Claude Code commands. We're grateful for the foundation provided by the original repository and the broader Claude Code community.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
=======
- **Issues**: [GitHub Issues](https://github.com/wshobson/commands/issues)
- **Contributions**: Pull requests welcome following the development guidelines
- **Questions**: Open a discussion in the repository
>>>>>>> upstream/main
