#!/usr/bin/env python3
"""
Initialize versioning for all existing commands
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from version_manager import VersionManager


def main():
    """Initialize version 1.0.0 for all commands"""
    repo_path = Path(__file__).parent.parent
    manager = VersionManager(repo_path)
    
    # Initialize workflows
    workflows_dir = repo_path / 'workflows'
    for workflow_file in workflows_dir.glob('*.md'):
        if workflow_file.stem not in manager.metadata:
            print(f"Initializing {workflow_file.stem}...")
            manager.initialize_command(
                workflow_file,
                description=f"Workflow: {workflow_file.stem.replace('-', ' ').title()}"
            )
    
    # Initialize tools
    tools_dir = repo_path / 'tools'
    for tool_file in tools_dir.glob('*.md'):
        if tool_file.stem not in manager.metadata:
            print(f"Initializing {tool_file.stem}...")
            manager.initialize_command(
                tool_file,
                description=f"Tool: {tool_file.stem.replace('-', ' ').title()}"
            )
    
    # Generate initial report
    print("\n" + "="*50)
    print(manager.generate_version_report())


if __name__ == '__main__':
    main()