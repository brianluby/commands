# Development Guide for Claude Code Commands

This guide covers development practices, testing, and quality standards for contributing to the commands repository.

## Getting Started

### Prerequisites
- Python 3.8+
- Git
- Claude Code installed
- (Optional) pre-commit for automated checks

### Setup
```bash
# Clone the repository
git clone https://github.com/brianluby/commands.git
cd commands

# Install development dependencies
pip install -r tests/requirements.txt

# Set up pre-commit hooks (recommended)
./scripts/setup-hooks.sh
```

## Project Structure

```
commands/
├── workflows/           # Multi-subagent orchestration commands
├── tools/              # Single-purpose utility commands  
├── tests/              # Test framework and validation
├── scripts/            # Development and maintenance scripts
├── templates/          # Command templates
├── docs/               # Documentation
├── .command-metadata.json  # Version and metadata tracking
├── .pre-commit-config.yaml # Pre-commit hook configuration
└── CHANGELOG.md        # Version history
```

## Creating New Commands

### 1. Choose Command Type

**Workflow** (multi-subagent coordination):
- Complex tasks requiring multiple specialists
- Problem-solving with unknown solutions
- Cross-domain implementations

**Tool** (single-purpose utility):
- Specific, well-defined tasks
- Direct implementation control
- Domain-specific operations

### 2. Use the Template

```bash
# Copy template
cp templates/command-template.md tools/my-new-command.md

# Edit with your implementation
# Remember to update version frontmatter
```

### 3. Follow Naming Conventions

- Use `lowercase-hyphen-names`
- Be descriptive but concise
- Match the filename to the command name
- Maximum 30 characters

### 4. Include Required Sections

Every command should have:
- Version frontmatter
- Clear description
- Usage examples
- Error handling
- Implementation details
- Related commands

### 5. Add Error Handling

Follow the patterns in `docs/ERROR_HANDLING.md`:
- Pre-flight checks
- Graceful failures
- Clear error messages
- Recovery suggestions

## Testing Commands

### Run Validation

```bash
# Validate single command
python tests/test_framework.py --path . --output report.md

# Validate all commands
./tests/run_tests.sh

# Use the validate-command slash command
/validate-command my-new-command
```

### Test Scenarios

Test your command with:
- ✓ Valid inputs
- ✓ Missing arguments
- ✓ Invalid arguments
- ✓ Missing dependencies
- ✓ Wrong directory context
- ✓ Permission issues
- ✓ Network failures (if applicable)

### Quality Checklist

Before submitting:
- [ ] Command validates without errors
- [ ] Version metadata is present
- [ ] Error handling is comprehensive
- [ ] Examples are clear and working
- [ ] Related commands are linked
- [ ] No broken references
- [ ] Markdown is properly formatted

## Version Management

### Initialize Version

```bash
# For new commands
python version_manager.py init tools/my-new-command.md \
  --description "Brief description" \
  --tags tag1 tag2 \
  --dependencies other-command
```

### Update Version

```bash
# Patch version (bug fixes)
python version_manager.py update my-new-command patch \
  --changes "Fixed error handling" "Updated documentation"

# Minor version (new features)
python version_manager.py update my-new-command minor \
  --changes "Added new option" "Enhanced performance"

# Major version (breaking changes)
python version_manager.py update my-new-command major \
  --changes "Redesigned API" \
  --breaking "Removed old syntax" "Changed parameter names"
```

## Pre-commit Hooks

Hooks run automatically on commit to:
- Validate command structure
- Check naming conventions
- Verify version metadata
- Format markdown
- Fix line endings

### Run Manually

```bash
# Run all hooks
pre-commit run --all-files

# Run specific hook
pre-commit run validate-commands

# Skip hooks (not recommended)
git commit --no-verify
```

## Best Practices

### Command Design

1. **Single Responsibility**: Each command does one thing well
2. **Composability**: Commands work together
3. **Predictability**: Consistent behavior and output
4. **Discoverability**: Clear names and descriptions

### Documentation

1. **Show, Don't Tell**: Include working examples
2. **Explain Why**: Context for design decisions
3. **Keep Updated**: Documentation matches implementation
4. **User-Focused**: Write for the end user

### Error Messages

1. **Be Specific**: "File not found" → "Config file 'package.json' not found"
2. **Be Helpful**: Always suggest next steps
3. **Be Honest**: Admit limitations
4. **Be Concise**: Scannable error output

### Subagent Usage (Workflows)

1. **Choose Appropriate Subagents**: Match expertise to task
2. **Handle Failures**: Plan for subagent unavailability
3. **Coordinate Effectively**: Clear task delegation
4. **Report Progress**: Keep user informed

## Testing Framework

### Unit Tests

```python
# tests/test_my_command.py
from test_framework import CommandValidator

def test_my_command_structure():
    validator = CommandValidator(Path("tools/my-command.md"))
    results = validator.validate()
    
    errors = [r for r in results if r.level == ValidationLevel.ERROR]
    assert len(errors) == 0, f"Found errors: {errors}"
```

### Integration Tests

Test command interactions:
```bash
# Test command pipeline
/api-scaffold user-service
/test-harness user-service
/security-scan user-service
/docker-optimize user-service
```

### Performance Tests

For resource-intensive commands:
- Measure execution time
- Check memory usage
- Validate output size
- Test with large inputs

## Debugging

### Enable Verbose Output

Add debug sections to commands:
```markdown
## Debug Mode
When --debug flag is present:
- Show all validation steps
- Log subagent communications
- Display intermediate results
- Keep temporary files
```

### Common Issues

**Command Not Found**
- Check file location
- Verify filename matches command
- Ensure .md extension

**Validation Failures**
- Run test framework for details
- Check for syntax errors
- Verify all required sections

**Subagent Failures**
- Check subagent availability
- Verify correct subagent_type
- Test with fallback options

## Contributing

### Process

1. Fork the repository
2. Create feature branch
3. Implement changes
4. Add/update tests
5. Update documentation
6. Run validation
7. Submit PR

### PR Checklist

- [ ] Meaningful commit messages
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Version bumped (if applicable)
- [ ] CHANGELOG updated
- [ ] No merge conflicts

### Code Review

Reviewers check for:
- Functionality correctness
- Error handling completeness
- Documentation clarity
- Integration compatibility
- Performance impact

## Maintenance

### Regular Tasks

Weekly:
- Review error reports
- Update dependencies
- Check for broken links

Monthly:
- Analyze usage patterns
- Update popular commands
- Archive deprecated commands

Quarterly:
- Major version planning
- Performance optimization
- Security audit

### Deprecation Process

1. Mark as deprecated in metadata
2. Add deprecation notice to command
3. Suggest alternatives
4. Maintain for 2 major versions
5. Move to archive/

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Subagents Repository](https://github.com/wshobson/agents)
- [Error Handling Guide](docs/ERROR_HANDLING.md)
- [Command Template](templates/command-template.md)

## Getting Help

- **Issues**: GitHub Issues for bugs/features
- **Discussions**: GitHub Discussions for questions
- **Documentation**: This guide and inline docs
- **Examples**: Existing commands as reference

Remember: Quality over quantity. A few well-crafted commands are better than many mediocre ones.