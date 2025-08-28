---
version: 1.0.0
tags: [validation, quality, testing]
---

# Validate Command

Comprehensive validation tool for Claude Code slash commands. Checks syntax, structure, best practices, and cross-command compatibility.

## Usage
```
/validate-command [command-name or "all"]
```

## Validation Checks

### Structural Validation
- ✓ Proper markdown formatting
- ✓ Required sections present
- ✓ Valid YAML frontmatter (if present)
- ✓ Consistent heading hierarchy

### Naming & Conventions
- ✓ Lowercase-hyphen naming
- ✓ Descriptive command name
- ✓ Appropriate command type (workflow vs tool)

### Content Validation
- ✓ $ARGUMENTS placeholder for parametric commands
- ✓ Clear usage examples
- ✓ Error handling sections
- ✓ No broken internal references

### Integration Checks
- ✓ Valid references to other commands
- ✓ Proper subagent_type for workflows
- ✓ Compatible dependency versions
- ✓ No circular dependencies

### Quality Metrics
- ✓ Documentation completeness
- ✓ Example coverage
- ✓ Error handling robustness
- ✓ Testability score

## Implementation

Given: $ARGUMENTS

I'll validate the specified command(s) using our comprehensive test framework.

### Step 1: Load Validation Framework

```python
import sys
from pathlib import Path

# Check if test framework exists
test_framework_path = Path("tests/test_framework.py")
if not test_framework_path.exists():
    print("❌ Test framework not found. Creating basic validator...")
    # Implement basic validation inline
else:
    sys.path.append("tests")
    from test_framework import CommandValidator, WorkflowValidator, CommandTestSuite
```

### Step 2: Determine Validation Scope

```python
# Parse arguments to determine what to validate
if not arguments or arguments.lower() == "all":
    # Validate all commands
    validate_all = True
    target_commands = []
else:
    # Validate specific command(s)
    validate_all = False
    target_commands = [cmd.strip() for cmd in arguments.split(",")]
```

### Step 3: Run Validation

For each command:
1. Locate command file
2. Determine command type (workflow/tool)
3. Apply appropriate validator
4. Collect results
5. Generate recommendations

### Step 4: Generate Report

```markdown
# Command Validation Report

## Summary
- Commands validated: [count]
- ✅ Passed: [count]
- ⚠️ Warnings: [count]
- ❌ Errors: [count]

## Detailed Results

### [Command Name]
**Status**: [Pass/Warning/Fail]
**Type**: [Workflow/Tool]
**Version**: [version]

#### Issues Found:
[List of issues with severity and line numbers]

#### Recommendations:
[Specific fixes for each issue]

#### Quality Score: [A-F rating]
- Documentation: [score]
- Error Handling: [score]
- Integration: [score]
- Maintainability: [score]
```

## Validation Rules

### Must Fix (Errors):
- Empty command files
- Invalid markdown syntax
- Missing $ARGUMENTS in parametric commands
- Circular dependencies
- Invalid version format

### Should Fix (Warnings):
- Missing usage examples
- No error handling section
- Undocumented parameters
- Very long command names
- Missing related commands section

### Nice to Have (Info):
- Could add more examples
- Consider adding video tutorial
- Tag suggestions for discoverability

## Quick Fixes

For common issues, I'll provide automatic fix commands:

```bash
# Add missing version
python version_manager.py init [command-path]

# Fix markdown formatting
prettier --write [command-path]

# Add error handling template
cat templates/error-handling-snippet.md >> [command-path]
```

## Integration with CI/CD

To add to your workflow:
```yaml
# .github/workflows/validate-commands.yml
name: Validate Commands
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate all commands
        run: |
          python tests/test_framework.py
```

## Error Recovery

If validation itself fails:
```
⚠️ Validation error: [error description]

This might be because:
- Test framework is not set up
- Python dependencies are missing
- File permissions issue

Quick fix:
pip install -r tests/requirements.txt
```

## Next Steps

After validation:
1. Fix any errors (required for PR merge)
2. Address warnings (recommended)
3. Consider info suggestions (optional)
4. Run validation in pre-commit hook
5. Add to CI/CD pipeline