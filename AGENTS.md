# AGENTS.md

## Repository Type
Collection of 52 production-ready slash commands for Claude Code organized as workflows (multi-subagent orchestration) and tools (single-purpose utilities).

## Build/Test Commands
This repository contains markdown-based slash commands - no build/test commands needed. Commands are validated through usage in Claude Code environment.

## File Structure
- `workflows/` - Multi-subagent orchestration commands (14 files)
- `tools/` - Single-purpose utility commands (38 files)
- Commands are markdown files where filename becomes the slash command

## Code Style Guidelines
- Use lowercase-hyphen-names for command files (e.g., `api-scaffold.md`)
- Include `$ARGUMENTS` placeholder for user input in command content
- Structure commands with clear sections: Context, Requirements, Instructions
- Follow markdown formatting with proper headers, code blocks, and examples
- Include comprehensive documentation with usage patterns and best practices
- Provide production-ready implementations with security and testing considerations
- Use framework auto-detection patterns to work with existing tech stacks

## Command Types
- **Workflows**: Use for complex, multi-domain tasks requiring subagent coordination
- **Tools**: Use for focused, single-domain tasks with specific implementations
- Commands should be self-contained and work together seamlessly