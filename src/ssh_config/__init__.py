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

__version__ = "0.1.0"

# Public API
__all__ = [
    "convert_format",
    "detect_format",
    "process_directory",
    "SSHConfigParser",
]