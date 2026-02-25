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

"""Simplified CLI using Typer."""

import json
import os
import sys
from pathlib import Path
from typing import Optional

import typer

# Add the src directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from ssh_config.core import convert_ssh_config


app = typer.Typer(
    name="ssh-config",
    help="SSH Config Tool - Convert between SSH config, YAML, and JSON formats.",
    add_completion=False,
)


@app.command()
def main(
    to_yaml: bool = typer.Option(False, "--to-yaml", help="Convert to YAML format"),
    to_json: bool = typer.Option(False, "--to-json", help="Convert to JSON format"),
    to_ssh: bool = typer.Option(False, "--to-ssh", help="Convert to SSH config format"),
    src: Optional[str] = typer.Option(None, "--src", help="Source file or directory path (default: ~/.ssh)"),
    dest: Optional[str] = typer.Option(None, "--dest", help="Destination file path (default: stdout)"),
):
    """Main entry point for the CLI."""
    # Determine target format
    target_format = None
    format_flags = [to_yaml, to_json, to_ssh]
    
    if sum(format_flags) == 0:
        # Default to YAML if no format specified
        target_format = "yaml"
        to_yaml = True
    elif sum(format_flags) == 1:
        if to_yaml:
            target_format = "yaml"
        elif to_json:
            target_format = "json"
        elif to_ssh:
            target_format = "ssh"
    else:
        typer.echo("Error: Please specify exactly one output format (--to-yaml, --to-json, or --to-ssh)", err=True)
        raise typer.Exit(code=1)
    
    # Check if input is from stdin
    if not sys.stdin.isatty():
        # Read from stdin
        content = sys.stdin.read()
        if not content.strip():
            typer.echo("Error: Empty input from stdin", err=True)
            raise typer.Exit(code=1)
        
        try:
            if to_yaml:
                result = convert_ssh_config(content, to_yaml=True)
            elif to_json:
                result = convert_ssh_config(content, to_json=True)
            elif to_ssh:
                result = convert_ssh_config(content, to_ssh=True)
            typer.echo(result, nl=False)
        except Exception as e:
            typer.echo(f"Error: {e}", err=True)
            raise typer.Exit(code=1)
    else:
        # File/directory mode
        if src is None:
            # Default to ~/.ssh directory
            src = os.path.expanduser("~/.ssh")
        
        src_path = Path(src)
        if not src_path.exists():
            typer.echo(f"Error: Source path '{src}' does not exist", err=True)
            raise typer.Exit(code=1)
        
        try:
            if src_path.is_file():
                with open(src_path, 'r') as f:
                    content = f.read()
                if to_yaml:
                    result = convert_ssh_config(content, to_yaml=True)
                elif to_json:
                    result = convert_ssh_config(content, to_json=True)
                elif to_ssh:
                    result = convert_ssh_config(content, to_ssh=True)
            elif src_path.is_dir():
                # For now, we'll just process the directory as a simple case
                # In a full implementation, you'd want to scan for SSH config files
                typer.echo(f"Error: Directory processing not fully implemented", err=True)
                raise typer.Exit(code=1)
            else:
                typer.echo(f"Error: '{src}' is neither a file nor a directory", err=True)
                raise typer.Exit(code=1)
            
            if dest:
                # Write to file
                dest_path = Path(dest)
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                with open(dest_path, 'w') as f:
                    f.write(result)
                typer.echo(f"File has been saved successfully")
                typer.echo(f"File path: {dest_path}")
            else:
                # Output to stdout
                typer.echo(result, nl=False)
                
        except Exception as e:
            typer.echo(f"Error: {e}", err=True)
            raise typer.Exit(code=1)


if __name__ == "__main__":
    app()