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

"""SSH Config Tool - Python SDK.

A command-line utility for managing SSH configuration files.
Convert between SSH config, YAML, and JSON formats.
"""

from .parser import (
    convert_format,
    detect_format,
    process_directory,
    SSHConfigParser,
)

import typer

__version__ = "0.1.0"

app = typer.Typer(
    name="ssh-config",
    help="SSH Config Tool - Convert between SSH config, YAML, and JSON formats.",
    add_completion=False,
)

@app.command()
def convert(
    input_file: str = typer.Argument(..., help="Input file path"),
    output_file: str = typer.Argument(..., help="Output file path"),
    from_format: str = typer.Option(None, "--from", "-f", help="Source format (ssh, yaml, json)"),
    to_format: str = typer.Option(None, "--to", "-t", help="Target format (ssh, yaml, json)"),
):
    """Convert SSH config between different formats."""
    try:
        # Auto-detect format if not specified
        source_format = from_format or detect_format(input_file)
        target_format = to_format or detect_format(output_file)
        
        result = convert_format(input_file, output_file, source_format, target_format)
        typer.echo(f"Successfully converted {source_format} to {target_format}: {result}")
    except Exception as e:
        typer.secho(f"Error: {str(e)}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)

@app.command()
def version():
    """Show the version of ssh-config tool."""
    typer.echo(f"ssh-config version {__version__}")

# Public API
__all__ = [
    "convert_format",
    "detect_format",
    "process_directory",
    "SSHConfigParser",
    "app",
]