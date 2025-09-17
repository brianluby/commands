# AGENTS.md

## Repository Type
**Hybrid Repository**: 
- `opencode-tools/` - Native conversational development assistants for OpenCode
- `legacy-claude-tools/` - Original 52 production-ready slash commands for Claude Code
- `workflows/` - Multi-subagent orchestration workflows (Claude Code)

## Build/Test Commands
This repository contains markdown-based slash commands - no build/test commands needed. Commands are validated through usage in Claude Code environment.

## File Structure
- `opencode-tools/` - Native OpenCode conversational development assistants
- `legacy-claude-tools/` - Original Claude Code slash commands (52 tools + 14 workflows)
- `workflows/` - Multi-subagent orchestration workflows for Claude Code
- Commands are markdown files optimized for their respective environments

## Code Style Guidelines
- Use lowercase-hyphen-names for command files (e.g., `api-scaffold.md`)
- Include `$ARGUMENTS` placeholder for user input in command content
- Structure commands with clear sections: Context, Requirements, Instructions
- Follow markdown formatting with proper headers, code blocks, and examples
- Include comprehensive documentation with usage patterns and best practices
- Provide production-ready implementations with security and testing considerations
- Use framework auto-detection patterns to work with existing tech stacks

## Command Types

### OpenCode Native Tools (New)
- **Conversational Development**: Natural language interface with context awareness
- **Progressive Building**: Incremental feature development through dialogue  
- **Codebase Integration**: Automatically detects and integrates with existing code
- **Examples**: API Generator, Security Auditor, Container Optimizer

### Claude Code Commands (Legacy)
- **Workflows**: Multi-domain tasks requiring subagent coordination
- **Tools**: Focused, single-domain tasks with specific implementations
- **Slash Interface**: Template-based execution with `$ARGUMENTS` placeholders
- **Examples**: /api-scaffold, /security-scan, /docker-optimize