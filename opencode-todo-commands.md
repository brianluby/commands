# OpenCode Adaptation TODO

## Overview
This repository contains 52 production-ready slash commands designed for Claude Code. The commands provide excellent patterns and implementations but need adaptation for OpenCode's architecture.

## Key Differences to Address

### Command Format
- **Current**: Markdown files with `$ARGUMENTS` placeholder in `~/.claude/` directory
- **Needed**: Convert to OpenCode's command format and execution model
- **Location**: Determine where OpenCode stores/executes commands

### Subagent Architecture
- **Current**: Relies on Claude Code's subagent orchestration system
- **Needed**: Adapt multi-agent workflows to OpenCode's capabilities
- **Impact**: 14 workflow commands need significant rework

### Execution Environment
- **Current**: Executes within Claude Code's sandbox environment
- **Needed**: Adapt to OpenCode's tool execution and file system access
- **Consideration**: May have different security/permission models

## Adaptation Strategy

### Phase 1: Core Tools (38 commands)
- Start with single-purpose tools in `tools/` directory
- Focus on commands that generate code/configs (api-scaffold, docker-optimize, k8s-manifest)
- These have less dependency on subagent orchestration

### Phase 2: Workflow Adaptation (14 commands)
- Analyze which workflows can be simplified to single-agent execution
- Identify which require OpenCode's equivalent of subagent coordination
- May need to break complex workflows into sequential tool executions

### Phase 3: Integration Patterns
- Adapt command chaining and orchestration patterns
- Update documentation and usage examples
- Test command interoperability in OpenCode environment

## High-Value Commands to Prioritize
1. `api-scaffold.md` - Production-ready API generation
2. `security-scan.md` - Comprehensive security analysis
3. `docker-optimize.md` - Container optimization
4. `k8s-manifest.md` - Kubernetes deployment configs
5. `test-harness.md` - Comprehensive testing setup

## Technical Changes Needed
- Replace `$ARGUMENTS` with OpenCode's parameter system
- Adapt framework auto-detection logic
- Update file path references and execution context
- Modify output formats to match OpenCode expectations
- Test tool integration and error handling