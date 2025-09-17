# Legacy Claude Code Commands
*Original Production-Ready Slash Commands*

## Overview
This directory contains the **original Claude Code commands** designed for the Claude Code environment with slash command interface and multi-subagent orchestration.

## Usage (Claude Code Environment)
These commands use the Claude Code slash command format:
```bash
/api-scaffold "FastAPI user management API with JWT auth"
/security-scan "comprehensive security audit for Python web application"
/docker-optimize "multi-stage Docker build for Node.js microservice"
```

## Command Structure
- **Tools** (38 commands): Single-purpose utilities for specific operations
- **Workflows** (14 commands): Multi-subagent orchestration for complex tasks

## Key Features
- `$ARGUMENTS` placeholder system
- Multi-subagent Task tool delegation
- Template-based rapid generation
- Production-ready implementations
- Comprehensive documentation

## Integration Patterns
Commands work together in workflows:
```bash
/api-scaffold → /test-harness → /security-scan → /docker-optimize → /k8s-manifest
```

## For OpenCode Users
If you're using OpenCode (not Claude Code), see the `opencode-tools/` directory for **conversational alternatives** specifically designed for OpenCode's natural language interface.

## Preserved Content
This directory preserves the complete original Claude Code command set for:
- Claude Code users who prefer slash commands
- Reference and learning purposes
- Migration planning from Claude Code to OpenCode
- Maintaining compatibility with existing workflows

---

*For OpenCode native tools optimized for conversational development, see the `opencode-tools/` directory.*