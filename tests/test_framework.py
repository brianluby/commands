#!/usr/bin/env python3
"""
Command Testing Framework for Claude Code Slash Commands

This framework validates:
- Command structure and syntax
- Required placeholders ($ARGUMENTS)
- Markdown formatting
- Command naming conventions
- Integration points between commands
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class CommandType(Enum):
    WORKFLOW = "workflow"
    TOOL = "tool"


class ValidationLevel(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationResult:
    level: ValidationLevel
    message: str
    line_number: Optional[int] = None
    command_file: Optional[str] = None


@dataclass
class CommandMetadata:
    name: str
    type: CommandType
    version: str = "1.0.0"
    description: str = ""
    dependencies: List[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.tags is None:
            self.tags = []


class CommandValidator:
    """Validates individual slash command files"""
    
    def __init__(self, command_path: Path):
        self.command_path = command_path
        self.command_name = command_path.stem
        self.content = command_path.read_text()
        self.lines = self.content.splitlines()
        self.results: List[ValidationResult] = []
        
    def validate(self) -> List[ValidationResult]:
        """Run all validations on the command"""
        self._validate_structure()
        self._validate_naming()
        self._validate_placeholders()
        self._validate_markdown()
        self._validate_references()
        self._validate_metadata()
        return self.results
    
    def _validate_structure(self):
        """Validate basic command structure"""
        if not self.content.strip():
            self.results.append(ValidationResult(
                ValidationLevel.ERROR,
                "Command file is empty",
                command_file=str(self.command_path)
            ))
            
        # Check for required sections
        if not any(line.startswith('#') for line in self.lines):
            self.results.append(ValidationResult(
                ValidationLevel.WARNING,
                "Command should have at least one header",
                command_file=str(self.command_path)
            ))
    
    def _validate_naming(self):
        """Validate command naming conventions"""
        # Check for lowercase-hyphen naming
        if not re.match(r'^[a-z][a-z0-9-]*$', self.command_name):
            self.results.append(ValidationResult(
                ValidationLevel.ERROR,
                f"Command name '{self.command_name}' must use lowercase-hyphen format",
                command_file=str(self.command_path)
            ))
            
        # Check name length
        if len(self.command_name) > 30:
            self.results.append(ValidationResult(
                ValidationLevel.WARNING,
                f"Command name '{self.command_name}' is longer than 30 characters",
                command_file=str(self.command_path)
            ))
    
    def _validate_placeholders(self):
        """Validate required placeholders"""
        has_arguments = '$ARGUMENTS' in self.content
        
        # Check if command likely needs arguments but doesn't have placeholder
        needs_arguments_keywords = [
            'create', 'generate', 'build', 'implement', 'add', 'modify',
            'analyze', 'review', 'optimize', 'migrate', 'convert'
        ]
        
        if any(keyword in self.command_name for keyword in needs_arguments_keywords):
            if not has_arguments:
                self.results.append(ValidationResult(
                    ValidationLevel.WARNING,
                    "Command likely needs $ARGUMENTS placeholder based on its name",
                    command_file=str(self.command_path)
                ))
    
    def _validate_markdown(self):
        """Validate markdown syntax and formatting"""
        # Check for unclosed code blocks
        code_block_count = self.content.count('```')
        if code_block_count % 2 != 0:
            self.results.append(ValidationResult(
                ValidationLevel.ERROR,
                "Unclosed code block detected",
                command_file=str(self.command_path)
            ))
            
        # Check for proper header hierarchy
        header_levels = []
        for i, line in enumerate(self.lines):
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                header_levels.append((level, i + 1))
        
        for i in range(1, len(header_levels)):
            curr_level, curr_line = header_levels[i]
            prev_level, _ = header_levels[i-1]
            
            if curr_level > prev_level + 1:
                self.results.append(ValidationResult(
                    ValidationLevel.WARNING,
                    f"Header level jumps from {prev_level} to {curr_level}",
                    line_number=curr_line,
                    command_file=str(self.command_path)
                ))
    
    def _validate_references(self):
        """Validate references to other commands and tools"""
        # Find references to other commands - more selective pattern
        # Only match /command-name at word boundaries, not URLs or paths
        command_pattern = r'(?:^|[\s`])(/[a-z][a-z0-9-]+)(?:[\s`]|$)'
        command_refs = re.findall(command_pattern, self.content, re.MULTILINE)
        
        # Common non-command patterns to exclude
        exclude_patterns = [
            '/localhost', '/bin', '/bash', '/usr', '/etc', '/var', '/tmp',
            '/pre-commit', '/checkout', '/upload', '/download', '/cli',
            '/setup-node', '/workflows', '/tools', '/actions', 
            # HTML tags
            '/div', '/span', '/button', '/form', '/label', '/input',
            '/h1', '/h2', '/h3', '/h4', '/h5', '/h6', '/p', '/a',
            '/title', '/head', '/body', '/style', '/script', '/fieldset',
            '/legend', '/stopped',
            # Common paths
            '/api', '/auth', '/user', '/admin', '/config'
        ]
        
        # Check if referenced commands exist
        base_path = self.command_path.parent.parent
        for ref_match in command_refs:
            ref = ref_match.strip('/ ')
            
            # Skip if it's the current command
            if ref == self.command_name:
                continue
            
            # Skip excluded patterns
            if any(f'/{ref}' in exclude_patterns or ref.startswith(ex.lstrip('/')) for ex in exclude_patterns):
                continue
                
            # Check in both workflows and tools
            workflow_path = base_path / 'workflows' / f'{ref}.md'
            tool_path = base_path / 'tools' / f'{ref}.md'
            
            if not workflow_path.exists() and not tool_path.exists():
                self.results.append(ValidationResult(
                    ValidationLevel.WARNING,
                    f"Referenced command '/{ref}' not found",
                    command_file=str(self.command_path)
                ))
    
    def _validate_metadata(self):
        """Validate command metadata if present"""
        # Look for metadata in YAML frontmatter
        if self.content.startswith('---') and HAS_YAML:
            try:
                end_index = self.content.find('---', 3)
                if end_index != -1:
                    metadata_str = self.content[3:end_index]
                    metadata = yaml.safe_load(metadata_str)
                    
                    # Validate version format
                    if 'version' in metadata:
                        if not re.match(r'^\d+\.\d+\.\d+$', str(metadata['version'])):
                            self.results.append(ValidationResult(
                                ValidationLevel.ERROR,
                                f"Invalid version format: {metadata['version']}",
                                command_file=str(self.command_path)
                            ))
            except yaml.YAMLError as e:
                self.results.append(ValidationResult(
                    ValidationLevel.ERROR,
                    f"Invalid YAML frontmatter: {e}",
                    command_file=str(self.command_path)
                ))


class WorkflowValidator(CommandValidator):
    """Validates workflow-specific requirements"""
    
    def validate(self) -> List[ValidationResult]:
        """Run workflow-specific validations"""
        super().validate()
        self._validate_task_tool_usage()
        self._validate_subagent_references()
        return self.results
    
    def _validate_task_tool_usage(self):
        """Validate proper Task tool usage in workflows"""
        # Check if workflow uses Task tool
        if 'Task tool' not in self.content and 'subagent' not in self.content.lower():
            self.results.append(ValidationResult(
                ValidationLevel.WARNING,
                "Workflow should use Task tool for subagent coordination",
                command_file=str(self.command_path)
            ))
            
        # Check for proper subagent_type specification
        if 'subagent_type' not in self.content and 'Task tool' in self.content:
            self.results.append(ValidationResult(
                ValidationLevel.WARNING,
                "Workflow using Task tool should specify subagent_type",
                command_file=str(self.command_path)
            ))
    
    def _validate_subagent_references(self):
        """Validate references to valid subagent types"""
        # Extract subagent types mentioned
        subagent_pattern = r'subagent_type["\s=:]+([a-z-]+)'
        subagent_refs = re.findall(subagent_pattern, self.content)
        
        # Known valid subagent types (from the documentation)
        valid_subagents = {
            'backend-architect', 'frontend-developer', 'test-automator',
            'deployment-engineer', 'debugger', 'performance-engineer',
            'security-auditor', 'code-reviewer', 'database-optimizer',
            'devops-troubleshooter', 'network-engineer', 'cloud-architect'
        }
        
        for subagent in subagent_refs:
            if subagent not in valid_subagents:
                self.results.append(ValidationResult(
                    ValidationLevel.WARNING,
                    f"Unknown subagent type: {subagent}",
                    command_file=str(self.command_path)
                ))


class CommandTestSuite:
    """Test suite for validating all commands in the repository"""
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.workflows_path = repo_path / 'workflows'
        self.tools_path = repo_path / 'tools'
        self.results: Dict[str, List[ValidationResult]] = {}
        
    def run_all_tests(self) -> Dict[str, List[ValidationResult]]:
        """Run validation on all commands"""
        # Validate workflows
        for workflow_file in self.workflows_path.glob('*.md'):
            validator = WorkflowValidator(workflow_file)
            self.results[str(workflow_file)] = validator.validate()
            
        # Validate tools
        for tool_file in self.tools_path.glob('*.md'):
            validator = CommandValidator(tool_file)
            self.results[str(tool_file)] = validator.validate()
            
        return self.results
    
    def generate_report(self) -> str:
        """Generate a human-readable test report"""
        report_lines = ["# Command Validation Report\n"]
        
        total_errors = 0
        total_warnings = 0
        total_info = 0
        
        for file_path, results in sorted(self.results.items()):
            if not results:
                continue
                
            file_errors = [r for r in results if r.level == ValidationLevel.ERROR]
            file_warnings = [r for r in results if r.level == ValidationLevel.WARNING]
            file_info = [r for r in results if r.level == ValidationLevel.INFO]
            
            total_errors += len(file_errors)
            total_warnings += len(file_warnings)
            total_info += len(file_info)
            
            if file_errors or file_warnings:
                report_lines.append(f"\n## {Path(file_path).name}")
                
                for result in results:
                    icon = {
                        ValidationLevel.ERROR: "❌",
                        ValidationLevel.WARNING: "⚠️",
                        ValidationLevel.INFO: "ℹ️"
                    }[result.level]
                    
                    line_info = f" (line {result.line_number})" if result.line_number else ""
                    report_lines.append(f"- {icon} {result.message}{line_info}")
        
        # Summary
        report_lines.insert(1, f"\n## Summary")
        report_lines.insert(2, f"- Total Commands: {len(self.results)}")
        report_lines.insert(3, f"- ❌ Errors: {total_errors}")
        report_lines.insert(4, f"- ⚠️  Warnings: {total_warnings}")
        report_lines.insert(5, f"- ℹ️  Info: {total_info}")
        report_lines.insert(6, "")
        
        return "\n".join(report_lines)
    
    def save_report(self, output_path: Path):
        """Save validation report to file"""
        report = self.generate_report()
        output_path.write_text(report)
        
    def get_exit_code(self) -> int:
        """Get exit code based on validation results"""
        for results in self.results.values():
            if any(r.level == ValidationLevel.ERROR for r in results):
                return 1
        return 0


def main():
    """Run command validation tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate Claude Code slash commands")
    parser.add_argument('--path', default='.', help='Path to commands repository')
    parser.add_argument('--output', help='Output file for validation report')
    parser.add_argument('--format', choices=['text', 'json'], default='text', 
                       help='Output format')
    
    args = parser.parse_args()
    
    repo_path = Path(args.path).resolve()
    test_suite = CommandTestSuite(repo_path)
    results = test_suite.run_all_tests()
    
    if args.format == 'json':
        # Convert results to JSON-serializable format
        json_results = {}
        for file_path, file_results in results.items():
            json_results[file_path] = [
                {
                    'level': r.level.value,
                    'message': r.message,
                    'line_number': r.line_number
                }
                for r in file_results
            ]
        
        if args.output:
            Path(args.output).write_text(json.dumps(json_results, indent=2))
        else:
            print(json.dumps(json_results, indent=2))
    else:
        if args.output:
            test_suite.save_report(Path(args.output))
            print(f"Validation report saved to: {args.output}")
        else:
            print(test_suite.generate_report())
    
    return test_suite.get_exit_code()


if __name__ == '__main__':
    exit(main())