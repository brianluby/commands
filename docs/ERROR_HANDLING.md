# Error Handling Standards for Claude Code Commands

This guide establishes error handling standards for all slash commands to ensure consistent, user-friendly error management.

## Core Principles

1. **Fail Gracefully**: Commands should never crash unexpectedly
2. **Clear Feedback**: Provide actionable error messages
3. **Recovery Paths**: Suggest fixes or alternatives when possible
4. **Context Preservation**: Don't lose user work due to errors

## Error Categories

### 1. Input Validation Errors
- Missing required arguments
- Invalid argument format
- Incompatible parameter combinations

**Standard Response:**
```markdown
❌ Invalid input: [specific issue]

Expected format:
/command-name <required-arg> [optional-arg]

Example:
/api-scaffold user management API with authentication

💡 Tip: [specific suggestion for fixing the input]
```

### 2. Environment Errors
- Missing dependencies
- Incorrect directory structure
- Permission issues

**Standard Response:**
```markdown
⚠️ Environment issue detected: [specific issue]

Required setup:
- [List of requirements]
- [How to install/fix]

Quick fix:
```bash
[command to fix the issue]
```

Would you like me to help set this up?
```

### 3. Integration Errors
- API failures
- Tool unavailability
- Network issues

**Standard Response:**
```markdown
🔌 Integration error: [service/tool] is not accessible

Possible causes:
- Service is down or unreachable
- Authentication/credentials issue
- Network connectivity problem

Alternatives:
1. [Alternative approach 1]
2. [Alternative approach 2]

Debug info: [error code/message if helpful]
```

### 4. Execution Errors
- Command failures
- Timeout issues
- Resource constraints

**Standard Response:**
```markdown
⚙️ Execution failed: [brief description]

What happened:
[Clear explanation of the failure]

Next steps:
1. [Immediate fix if possible]
2. [Alternative approach]
3. [How to get more help]

Debug command:
```bash
[command to investigate further]
```
```

## Implementation Patterns

### Pattern 1: Pre-flight Checks
Commands should validate environment before execution:

```markdown
## Pre-execution Validation

1. Check for required tools:
   - Verify Docker is installed for containerization commands
   - Check Node.js version for JavaScript projects
   - Ensure Git is configured for version control operations

2. Validate project structure:
   - Confirm we're in the right directory
   - Check for expected files (package.json, Dockerfile, etc.)
   - Verify permissions for file operations

3. Test connectivity:
   - API endpoints for external services
   - Database connections
   - Required authentication
```

### Pattern 2: Progressive Enhancement
Start with basic functionality and add features as available:

```markdown
## Progressive Feature Detection

Base functionality:
- [Core feature that always works]

Enhanced features (if available):
- ✅ Feature A (detected)
- ❌ Feature B (not available - [install link])
- ✅ Feature C (detected)

Proceeding with available features...
```

### Pattern 3: Fallback Strategies
Always have a Plan B:

```markdown
## Fallback Approaches

Primary approach failed: [what failed]

Trying alternative approach:
- Using [alternative tool/method]
- This may be slower/less optimal but will work
- Results will be functionally equivalent

[Proceed with alternative]
```

## Command-Specific Guidelines

### Workflows
- Must handle subagent failures gracefully
- Should report which subagents succeeded/failed
- Provide partial results when possible

### Tools
- Validate all inputs before processing
- Check tool availability early
- Offer manual alternatives for automation failures

## Error Message Templates

### Missing Dependency
```markdown
📦 Missing dependency: [package/tool name]

This command requires [tool] to be installed.

Install with:
```bash
# macOS
brew install [tool]

# Ubuntu/Debian  
sudo apt-get install [tool]

# npm/yarn (if applicable)
npm install -g [tool]
```

After installation, please run the command again.
```

### File Not Found
```markdown
📁 File not found: [filename]

I couldn't find the expected file at: [path]

Possible issues:
- Wrong directory (current: [pwd])
- File was moved or deleted
- Typo in filename

Suggestions:
1. Check if you're in the right directory
2. Use `/ls` to list available files
3. Search for similar files: `/search [partial-name]`
```

### Permission Denied
```markdown
🔒 Permission denied: [operation]

Unable to [action] due to insufficient permissions.

To fix:
1. Check file ownership: `ls -la [file]`
2. Update permissions: `chmod +x [file]`
3. Run with appropriate privileges (if needed)

⚠️ Be cautious when changing permissions or using elevated privileges.
```

### API/Network Error
```markdown
🌐 Network error: [service/endpoint]

Failed to connect to [service].

Status: [HTTP status code if applicable]
Error: [error message]

Troubleshooting:
1. Check internet connectivity
2. Verify service status: [status page URL]
3. Check authentication/API keys
4. Try again in a few moments

Alternative: [offline alternative if available]
```

## Best Practices

1. **Be Specific**: "File not found" → "Config file 'tsconfig.json' not found in /src"
2. **Be Helpful**: Always suggest next steps
3. **Be Honest**: Admit when something can't be fixed automatically
4. **Be Concise**: Error messages should be scannable
5. **Use Emojis Sparingly**: One emoji per error type for visual scanning

## Testing Error Handling

Commands should be tested with:
- Missing arguments
- Invalid inputs
- Missing dependencies
- Network failures
- Permission issues
- Malformed data

## Recovery Mechanisms

### State Preservation
```markdown
💾 Saving progress before error handling...

Progress saved:
- ✅ Step 1: Completed
- ✅ Step 2: Completed  
- ❌ Step 3: Failed (current)
- ⏸️ Step 4: Pending

You can resume from Step 3 by running:
/resume-task [task-id]
```

### Rollback Support
```markdown
↩️ Error encountered. Rolling back changes...

Rolled back:
- Reverted file changes
- Cleaned up temporary files
- Restored original configuration

System is back to original state.
```

## Logging and Debugging

### Debug Mode
Commands should support verbose output:
```markdown
Running in debug mode (--debug flag detected)

[VERBOSE] Checking environment...
[VERBOSE] Found Node.js v18.0.0
[VERBOSE] Found npm v9.0.0
[ERROR] Docker not found in PATH
[VERBOSE] Attempted paths: /usr/local/bin, /usr/bin
```

### Error Reporting
For complex errors, provide a way to generate detailed reports:
```markdown
🐛 Unexpected error occurred

Error summary: [brief description]

To help us improve, you can:
1. Generate error report: `/generate-error-report`
2. Check known issues: [GitHub issues URL]
3. Get help: [support channel]

Error ID: [generated UUID for tracking]
```

## Integration with Subagents

When using subagents in workflows:

```markdown
## Subagent Coordination Errors

Subagent 'backend-architect' failed:
- Task: Design API structure
- Error: Invalid OpenAPI specification
- Impact: Frontend development blocked

Mitigation:
1. Using fallback template for API design
2. Frontend can proceed with mock data
3. Manual API review recommended

Continue with partial results? (y/n)
```

## Summary

Good error handling:
- Prevents user frustration
- Enables self-service problem solving  
- Maintains command reliability
- Improves user trust
- Facilitates debugging

Remember: Every error is an opportunity to help the user succeed despite obstacles.