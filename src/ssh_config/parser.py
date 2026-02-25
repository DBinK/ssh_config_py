# Copyright 2026 Your Name
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""SSH configuration parser and converter.

This module provides functionality to parse and convert between SSH config,
YAML, and JSON formats.
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Union

import yaml


class SSHConfigParser:
    """Parser for SSH configuration files."""

    @staticmethod
    def parse_ssh_config(content: str) -> List[Dict[str, Any]]:
        """Parse SSH config format into structured data."""
        hosts = []
        current_host = None
        
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
                
            # Handle Host directive
            if line.lower().startswith("host "):
                if current_host:
                    hosts.append(current_host)
                host_names = line[5:].strip().split()
                current_host = {"Host": host_names if len(host_names) > 1 else host_names[0]}
            elif current_host is not None:
                # Handle key-value pairs
                if " " in line:
                    key, value = line.split(" ", 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Handle multi-value keys (like IdentityFile)
                    if key in current_host:
                        if isinstance(current_host[key], list):
                            current_host[key].append(value)
                        else:
                            current_host[key] = [current_host[key], value]
                    else:
                        current_host[key] = value
        
        if current_host:
            hosts.append(current_host)
            
        return hosts

    @staticmethod
    def format_ssh_config(data: List[Dict[str, Any]]) -> str:
        """Format structured data back to SSH config format."""
        lines = []
        
        for host in data:
            if isinstance(host.get("Host"), list):
                host_line = "Host " + " ".join(host["Host"])
            else:
                host_line = f"Host {host['Host']}"
            lines.append(host_line)
            
            for key, value in host.items():
                if key == "Host":
                    continue
                    
                if isinstance(value, list):
                    for item in value:
                        lines.append(f"    {key} {item}")
                else:
                    lines.append(f"    {key} {value}")
            lines.append("")  # Empty line between hosts
            
        return "\n".join(lines).rstrip() + "\n"


def detect_format(content: str) -> str:
    """Detect the format of the input content.
    
    Returns:
        str: One of 'ssh', 'yaml', 'json'
    """
    content = content.strip()
    if not content:
        return 'ssh'
    
    # Try JSON first
    try:
        json.loads(content)
        return 'json'
    except json.JSONDecodeError:
        pass
    
    # Try YAML next
    try:
        yaml.safe_load(content)
        # Additional check: if it looks like SSH config, prefer SSH
        if _looks_like_ssh_config(content):
            return 'ssh'
        return 'yaml'
    except yaml.YAMLError:
        pass
    
    # Default to SSH config
    return 'ssh'


def _looks_like_ssh_config(content: str) -> bool:
    """Check if content looks like SSH config format."""
    lines = content.splitlines()
    for line in lines[:10]:  # Check first 10 lines
        line = line.strip()
        if line and not line.startswith("#"):
            if line.lower().startswith(("host ", "match ")):
                return True
            if " " in line and not line.startswith(("{", "[", "-")):
                # Key-value pair without YAML/JSON syntax
                return True
    return False


def convert_format(content: str, target_format: str, source_format: str = None) -> str:
    """Convert content between formats.
    
    Args:
        content: Input content as string
        target_format: Target format ('ssh', 'yaml', 'json')
        source_format: Source format (auto-detected if None)
    
    Returns:
        Converted content as string
    """
    if source_format is None:
        source_format = detect_format(content)
    
    if source_format == target_format:
        return content
    
    # Parse to intermediate format (list of dicts)
    if source_format == 'ssh':
        data = SSHConfigParser.parse_ssh_config(content)
    elif source_format == 'yaml':
        data = yaml.safe_load(content)
    elif source_format == 'json':
        data = json.loads(content)
    else:
        raise ValueError(f"Unsupported source format: {source_format}")
    
    # Convert to target format
    if target_format == 'ssh':
        return SSHConfigParser.format_ssh_config(data)
    elif target_format == 'yaml':
        return yaml.dump(data, default_flow_style=False, indent=2)
    elif target_format == 'json':
        return json.dumps(data, indent=2)
    else:
        raise ValueError(f"Unsupported target format: {target_format}")


def process_directory(directory: Union[str, Path]) -> List[Dict[str, Any]]:
    """Process all SSH config files in a directory.
    
    Skips files that look like private keys or other non-config files.
    """
    directory = Path(directory)
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    config_files = []
    skip_patterns = [
        r'.*\.pub$',  # Public keys
        r'id_.*',     # Private keys
        r'.*\.pem$',  # PEM files
        r'known_hosts',
        r'authorized_keys',
    ]
    
    for file_path in directory.rglob('*'):
        if file_path.is_file():
            # Skip non-config files
            should_skip = False
            for pattern in skip_patterns:
                if re.match(pattern, file_path.name, re.IGNORECASE):
                    should_skip = True
                    break
            
            if not should_skip:
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        if detect_format(content) == 'ssh':
                            config_files.extend(SSHConfigParser.parse_ssh_config(content))
                except (UnicodeDecodeError, OSError):
                    # Skip binary files or unreadable files
                    continue
    
    return config_files