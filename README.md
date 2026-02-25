# SSH Config Tool - Python Version

A Python implementation of the SSH Config Tool that provides both a **SDK library** and **CLI tool** for managing SSH configuration files.

## Inspiration

This project is inspired by and reimplemented from the original [Go version](https://github.com/soulteary/ssh-config) by [Su Yang (soulteary)](https://github.com/soulteary). The Python version maintains the same functionality while providing a more accessible codebase for Python developers and enabling easy integration as an SDK library.

## Features

- ✅ Converts between SSH config, YAML, and JSON formats
- ✅ Automatic format detection
- ✅ Supports file input/output and stdin/stdout piping
- ✅ SDK for programmatic use in Python applications
- ✅ CLI tool with the same interface as the original Go version

## Installation

### From PyPI (when published)
```bash
pip install ssh-config
```

### From source
```bash
git clone https://github.com/your-username/ssh-config.git
cd ssh-config/ssh_config
uv sync --all-extras
```

## Usage

### As a CLI Tool

```bash
# Convert SSH config to YAML (default behavior)
ssh-config

# Convert from file to YAML
ssh-config --to-yaml --src ~/.ssh/config

# Convert YAML to SSH config
ssh-config --to-ssh --src config.yaml --dest ~/.ssh/config

# Use with pipes
cat input.conf | ssh-config --to-yaml > output.yaml
```

### As a Python SDK

```python
from ssh_config import convert_ssh_config, SSHConfigConverter

# Simple conversion using convenience function
ssh_content = "Host example.com\n    HostName example.com"
yaml_result = convert_ssh_config(ssh_content, to_yaml=True)

# Using the converter class for more control
converter = SSHConfigConverter()
detected_format = converter.detect_format(ssh_content)
yaml_result = converter.convert(ssh_content, "yaml")
```

## API Reference

### `convert_ssh_config(input_content: str, to_yaml: bool = False, to_json: bool = False, to_ssh: bool = False) -> str`

Convenience function to convert SSH configuration content between formats.

**Parameters:**
- `input_content`: The input content as a string
- `to_yaml`: Convert to YAML format
- `to_json`: Convert to JSON format  
- `to_ssh`: Convert to SSH config format

**Returns:** Converted content as a string

### `SSHConfigConverter` Class

Provides more granular control over the conversion process.

**Methods:**
- `detect_format(content: str) -> str`: Automatically detect input format
- `convert(input_content: str, target_format: str) -> str`: Convert to specified format
- `ssh_to_dict(content: str) -> Dict`: Parse SSH config to dictionary
- `dict_to_ssh(data: Dict) -> str`: Convert dictionary to SSH config
- `yaml_to_dict(content: str) -> Dict`: Parse YAML to dictionary
- `dict_to_yaml(data: Dict) -> str`: Convert dictionary to YAML
- `json_to_dict(content: str) -> Dict`: Parse JSON to dictionary  
- `dict_to_json(data: Dict) -> str`: Convert dictionary to JSON

## Development

### Dependencies
- Python 3.8+
- uv (for dependency management)

### Setup
```bash
uv sync --all-extras
```

### Testing
```bash
uv run pytest
```

### Building
```bash
uv build
```

## License

This project is licensed under the **Apache License, Version 2.0** (the "License"). You may not use this file except in compliance with the License. You may obtain a copy of the License at:

```
http://www.apache.org/licenses/LICENSE-2.0
```

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

The original Go implementation by [soulteary](https://github.com/soulteary) is also licensed under Apache-2.0, and this Python reimplementation maintains the same licensing terms.

## Credits

- Original Go implementation: [soulteary/ssh-config](https://github.com/soulteary/ssh-config)
- OpenSSH documentation: https://man.openbsd.org/ssh_config
- Inspiration for configuration file definition: https://github.com/bencromwell/sshush