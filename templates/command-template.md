---
version: 1.0.0
tags: [template, example]
---

# [Command Name]

[Brief description of what this command does]

## Usage
```
/command-name [arguments]
```

## Pre-flight Checks

Before proceeding, I'll verify:
1. Required tools and dependencies
2. Project structure and context
3. Necessary permissions

## Error Handling

### Missing Arguments
If no arguments provided:
```
❌ Missing required arguments

Usage: /command-name <required-arg> [optional-arg]

Example: /command-name "user authentication" --type jwt
```

### Environment Issues
I'll check for and handle:
- Missing dependencies → Provide installation instructions
- Wrong directory → Guide to correct location
- Permission issues → Suggest fixes

### Execution Failures
If any step fails, I'll:
- Provide clear error explanation
- Suggest alternative approaches
- Preserve any partial progress

## Process

1. **Validation Phase**
   - Validate input arguments
   - Check environment setup
   - Verify tool availability

2. **Execution Phase**
   - [Main task steps]
   - Progress updates after each major step
   - Error handling at each critical point

3. **Completion Phase**
   - Summary of what was accomplished
   - Any warnings or recommendations
   - Next steps for the user

## Implementation

Given the context:
$ARGUMENTS

I'll now:
[Specific steps based on user input]

## Fallback Strategies

If primary approach fails:
1. [Alternative method 1]
2. [Alternative method 2]
3. Manual instructions as last resort

## Success Criteria

The command succeeds when:
- [ ] All required files are created/updated
- [ ] No critical errors occurred
- [ ] Output passes validation
- [ ] User can proceed with next steps

## Related Commands

- `/related-command-1` - For [related task]
- `/related-command-2` - For [complementary task]