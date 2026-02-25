"""SSH Config Tool - Python SDK for managing SSH configuration files."""

from .core import SSHConfigConverter, convert_ssh_config

__version__ = "0.1.0"
__all__ = ["SSHConfigConverter", "convert_ssh_config"]