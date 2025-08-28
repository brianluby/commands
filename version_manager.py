#!/usr/bin/env python3
"""
Command Version Manager for Claude Code Slash Commands

Manages semantic versioning for commands and tracks changes.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class ChangeType(Enum):
    MAJOR = "major"  # Breaking changes
    MINOR = "minor"  # New features, backward compatible
    PATCH = "patch"  # Bug fixes


@dataclass
class CommandVersion:
    """Represents a command's version information"""
    version: str
    released: str
    changes: List[str]
    breaking_changes: List[str] = None
    deprecated_features: List[str] = None
    
    def __post_init__(self):
        if self.breaking_changes is None:
            self.breaking_changes = []
        if self.deprecated_features is None:
            self.deprecated_features = []


@dataclass
class CommandMetadata:
    """Complete metadata for a command"""
    name: str
    type: str  # workflow or tool
    description: str
    current_version: str
    created: str
    last_updated: str
    tags: List[str]
    dependencies: List[str]
    version_history: List[CommandVersion]


class VersionManager:
    """Manages versioning for all commands"""
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.metadata_file = repo_path / '.command-metadata.json'
        self.metadata = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, CommandMetadata]:
        """Load command metadata from file"""
        if self.metadata_file.exists():
            data = json.loads(self.metadata_file.read_text())
            return {
                name: CommandMetadata(**cmd_data)
                for name, cmd_data in data.items()
            }
        return {}
    
    def _save_metadata(self):
        """Save metadata to file"""
        data = {
            name: asdict(metadata)
            for name, metadata in self.metadata.items()
        }
        self.metadata_file.write_text(json.dumps(data, indent=2))
    
    def _parse_version(self, version: str) -> Tuple[int, int, int]:
        """Parse semantic version string"""
        match = re.match(r'^(\d+)\.(\d+)\.(\d+)$', version)
        if not match:
            raise ValueError(f"Invalid version format: {version}")
        return tuple(int(x) for x in match.groups())
    
    def _increment_version(self, version: str, change_type: ChangeType) -> str:
        """Increment version based on change type"""
        major, minor, patch = self._parse_version(version)
        
        if change_type == ChangeType.MAJOR:
            return f"{major + 1}.0.0"
        elif change_type == ChangeType.MINOR:
            return f"{major}.{minor + 1}.0"
        else:  # PATCH
            return f"{major}.{minor}.{patch + 1}"
    
    def initialize_command(self, command_path: Path, description: str = "",
                          tags: List[str] = None, dependencies: List[str] = None):
        """Initialize versioning for a new command"""
        command_name = command_path.stem
        command_type = "workflow" if "workflows" in str(command_path) else "tool"
        
        if command_name in self.metadata:
            print(f"Command {command_name} already initialized")
            return
        
        self.metadata[command_name] = CommandMetadata(
            name=command_name,
            type=command_type,
            description=description,
            current_version="1.0.0",
            created=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat(),
            tags=tags or [],
            dependencies=dependencies or [],
            version_history=[
                CommandVersion(
                    version="1.0.0",
                    released=datetime.now().isoformat(),
                    changes=["Initial release"]
                )
            ]
        )
        
        self._save_metadata()
        self._update_command_file(command_path, "1.0.0")
        print(f"Initialized {command_name} at version 1.0.0")
    
    def update_version(self, command_name: str, change_type: ChangeType,
                      changes: List[str], breaking_changes: List[str] = None,
                      deprecated_features: List[str] = None):
        """Update command version"""
        if command_name not in self.metadata:
            raise ValueError(f"Command {command_name} not found in metadata")
        
        metadata = self.metadata[command_name]
        old_version = metadata.current_version
        new_version = self._increment_version(old_version, change_type)
        
        # Create version entry
        version_entry = CommandVersion(
            version=new_version,
            released=datetime.now().isoformat(),
            changes=changes,
            breaking_changes=breaking_changes or [],
            deprecated_features=deprecated_features or []
        )
        
        # Update metadata
        metadata.current_version = new_version
        metadata.last_updated = datetime.now().isoformat()
        metadata.version_history.append(version_entry)
        
        # Save and update file
        self._save_metadata()
        
        # Find command file
        command_path = self._find_command_file(command_name)
        if command_path:
            self._update_command_file(command_path, new_version)
        
        print(f"Updated {command_name} from {old_version} to {new_version}")
        
        # Generate changelog entry
        self._update_changelog(command_name, old_version, new_version, version_entry)
    
    def _find_command_file(self, command_name: str) -> Optional[Path]:
        """Find the command file path"""
        for directory in ['workflows', 'tools']:
            path = self.repo_path / directory / f"{command_name}.md"
            if path.exists():
                return path
        return None
    
    def _update_command_file(self, command_path: Path, version: str):
        """Update version in command file"""
        content = command_path.read_text()
        
        # Check if file has YAML frontmatter
        if content.startswith('---'):
            # Update existing frontmatter
            end_index = content.find('---', 3)
            if end_index != -1:
                frontmatter = content[3:end_index]
                # Simple version update (proper YAML parsing would be better)
                if 'version:' in frontmatter:
                    frontmatter = re.sub(
                        r'version:\s*[\d.]+',
                        f'version: {version}',
                        frontmatter
                    )
                else:
                    frontmatter = f"{frontmatter.rstrip()}\nversion: {version}\n"
                
                new_content = f"---{frontmatter}---{content[end_index+3:]}"
            else:
                # Invalid frontmatter, add new one
                new_content = f"---\nversion: {version}\n---\n{content}"
        else:
            # Add frontmatter
            new_content = f"---\nversion: {version}\n---\n{content}"
        
        command_path.write_text(new_content)
    
    def _update_changelog(self, command_name: str, old_version: str, 
                         new_version: str, version_entry: CommandVersion):
        """Update CHANGELOG.md with version information"""
        changelog_path = self.repo_path / 'CHANGELOG.md'
        
        # Create changelog entry
        entry_lines = [
            f"\n## [{command_name}] {new_version} - {datetime.now().strftime('%Y-%m-%d')}\n"
        ]
        
        if version_entry.breaking_changes:
            entry_lines.append("\n### Breaking Changes\n")
            for change in version_entry.breaking_changes:
                entry_lines.append(f"- {change}\n")
        
        if version_entry.changes:
            entry_lines.append("\n### Changes\n")
            for change in version_entry.changes:
                entry_lines.append(f"- {change}\n")
        
        if version_entry.deprecated_features:
            entry_lines.append("\n### Deprecated\n")
            for feature in version_entry.deprecated_features:
                entry_lines.append(f"- {feature}\n")
        
        entry = "".join(entry_lines)
        
        # Update or create changelog
        if changelog_path.exists():
            content = changelog_path.read_text()
            # Insert after header
            lines = content.split('\n')
            insert_index = 0
            for i, line in enumerate(lines):
                if line.startswith('# '):
                    insert_index = i + 1
                    break
            
            lines.insert(insert_index, entry)
            changelog_path.write_text('\n'.join(lines))
        else:
            # Create new changelog
            changelog_content = f"# Claude Code Commands Changelog\n{entry}"
            changelog_path.write_text(changelog_content)
    
    def check_compatibility(self, command_name: str, required_version: str) -> bool:
        """Check if current command version satisfies requirement"""
        if command_name not in self.metadata:
            return False
        
        current = self._parse_version(self.metadata[command_name].current_version)
        required = self._parse_version(required_version)
        
        # Simple compatibility check: current >= required
        return current >= required
    
    def generate_version_report(self) -> str:
        """Generate a report of all command versions"""
        lines = ["# Command Version Report\n"]
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Group by type
        workflows = {k: v for k, v in self.metadata.items() if v.type == "workflow"}
        tools = {k: v for k, v in self.metadata.items() if v.type == "tool"}
        
        if workflows:
            lines.append("\n## Workflows\n")
            for name, metadata in sorted(workflows.items()):
                lines.append(f"- **{name}** (v{metadata.current_version})")
                if metadata.description:
                    lines.append(f"  - {metadata.description}")
                lines.append(f"  - Last updated: {metadata.last_updated[:10]}")
                lines.append("")
        
        if tools:
            lines.append("\n## Tools\n")
            for name, metadata in sorted(tools.items()):
                lines.append(f"- **{name}** (v{metadata.current_version})")
                if metadata.description:
                    lines.append(f"  - {metadata.description}")
                lines.append(f"  - Last updated: {metadata.last_updated[:10]}")
                lines.append("")
        
        return "\n".join(lines)


def main():
    """CLI for version management"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage Claude Code command versions")
    parser.add_argument('--path', default='.', help='Path to commands repository')
    
    subparsers = parser.add_subparsers(dest='action', help='Action to perform')
    
    # Initialize command
    init_parser = subparsers.add_parser('init', help='Initialize versioning for a command')
    init_parser.add_argument('command', help='Command file path')
    init_parser.add_argument('--description', help='Command description')
    init_parser.add_argument('--tags', nargs='+', help='Command tags')
    init_parser.add_argument('--dependencies', nargs='+', help='Command dependencies')
    
    # Update version
    update_parser = subparsers.add_parser('update', help='Update command version')
    update_parser.add_argument('command', help='Command name')
    update_parser.add_argument('type', choices=['major', 'minor', 'patch'])
    update_parser.add_argument('--changes', nargs='+', required=True, help='List of changes')
    update_parser.add_argument('--breaking', nargs='+', help='Breaking changes')
    update_parser.add_argument('--deprecated', nargs='+', help='Deprecated features')
    
    # Generate report
    report_parser = subparsers.add_parser('report', help='Generate version report')
    
    args = parser.parse_args()
    
    if not args.action:
        parser.print_help()
        return
    
    manager = VersionManager(Path(args.path))
    
    if args.action == 'init':
        command_path = Path(args.command)
        manager.initialize_command(
            command_path,
            description=args.description or "",
            tags=args.tags,
            dependencies=args.dependencies
        )
    elif args.action == 'update':
        manager.update_version(
            args.command,
            ChangeType(args.type),
            changes=args.changes,
            breaking_changes=args.breaking,
            deprecated_features=args.deprecated
        )
    elif args.action == 'report':
        print(manager.generate_version_report())


if __name__ == '__main__':
    main()