# SSH Config Tool - Python 版本

SSH Config Tool 的 Python 实现，同时提供 **SDK 库** 和 **CLI 工具** 来管理 SSH 配置文件。

## 项目灵感

本项目受 [Su Yang (soulteary)](https://github.com/soulteary) 的原始 [Go 版本](https://github.com/soulteary/ssh-config) 启发并重新实现。Python 版本保持了相同的功能，同时为 Python 开发者提供了更易访问的代码库，并支持作为 SDK 库轻松集成。

## 功能特性

- ✅ 在 SSH config、YAML 和 JSON 格式之间相互转换
- ✅ 自动格式检测
- ✅ 支持文件输入/输出和 stdin/stdout 管道
- ✅ 作为 Python 应用程序的 SDK
- ✅ CLI 工具，接口与原始 Go 版本相同

## 安装

### 从 PyPI 安装（发布后）
```bash
pip install ssh-config
```

### 从源码安装
```bash
git clone https://github.com/your-username/ssh-config.git
cd ssh-config/ssh_config
uv sync --all-extras
```

## 使用方法

### 作为 CLI 工具

```bash
# 转换 SSH config 为 YAML（默认行为）
ssh-config

# 从文件转换为 YAML
ssh-config --to-yaml --src ~/.ssh/config

# 转换 YAML 为 SSH config
ssh-config --to-ssh --src config.yaml --dest ~/.ssh/config

# 使用管道
cat input.conf | ssh-config --to-yaml > output.yaml
```

### 作为 Python SDK

```python
from ssh_config import convert_ssh_config, SSHConfigConverter

# 使用便捷函数进行简单转换
ssh_content = "Host example.com\n    HostName example.com"
yaml_result = convert_ssh_config(ssh_content, to_yaml=True)

# 使用转换器类进行更精细的控制
converter = SSHConfigConverter()
detected_format = converter.detect_format(ssh_content)
yaml_result = converter.convert(ssh_content, "yaml")
```

## API 参考

### `convert_ssh_config(input_content: str, to_yaml: bool = False, to_json: bool = False, to_ssh: bool = False) -> str`

用于在不同格式之间转换 SSH 配置内容的便捷函数。

**参数:**
- `input_content`: 输入内容字符串
- `to_yaml`: 转换为 YAML 格式
- `to_json`: 转换为 JSON 格式  
- `to_ssh`: 转换为 SSH config 格式

**返回值:** 转换后的内容字符串

### `SSHConfigConverter` 类

提供对转换过程的更精细控制。

**方法:**
- `detect_format(content: str) -> str`: 自动检测输入格式
- `convert(input_content: str, target_format: str) -> str`: 转换为指定格式
- `ssh_to_dict(content: str) -> Dict`: 解析 SSH config 为字典
- `dict_to_ssh(data: Dict) -> str`: 转换字典为 SSH config
- `yaml_to_dict(content: str) -> Dict`: 解析 YAML 为字典
- `dict_to_yaml(data: Dict) -> str`: 转换字典为 YAML
- `json_to_dict(content: str) -> Dict`: 解析 JSON 为字典  
- `dict_to_json(data: Dict) -> str`: 转换字典为 JSON

## 开发

### 依赖
- Python 3.8+
- uv（用于依赖管理）

### 设置
```bash
uv sync --all-extras
```

### 测试
```bash
uv run pytest
```

### 构建
```bash
uv build
```

## 许可证

Apache License 2.0 - 与原始 Go 项目相同。

## 致谢

- 原始 Go 实现: [soulteary/ssh-config](https://github.com/soulteary/ssh-config)
- OpenSSH 文档: https://man.openbsd.org/ssh_config
- 配置文件定义的灵感来源: https://github.com/bencromwell/sshush