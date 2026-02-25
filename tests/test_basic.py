import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from ssh_config.core import SSHConfigConverter, convert_ssh_config


def test_ssh_to_yaml():
    """测试SSH Config转YAML"""
    ssh_content = """Host example.com
    HostName example.com
    User admin
    Port 2222
"""
    
    converter = SSHConfigConverter()
    yaml_content = converter.convert(ssh_content, "yaml")
    print(yaml_content)

    # 验证YAML内容包含必要的字段
    assert "hosts:" in yaml_content
    assert "example.com" in yaml_content


def test_yaml_to_ssh():
    """测试YAML转SSH Config"""
    yaml_content = """hosts:
- Host: example.com
  HostName: example.com
  User: admin
  Port: "2222"
"""
    
    converter = SSHConfigConverter()
    ssh_content = converter.convert(yaml_content, "ssh")
    print(ssh_content)
    
    # 验证SSH内容
    assert "Host example.com" in ssh_content
    assert "HostName example.com" in ssh_content


def test_convert_function():
    """测试便捷转换函数"""
    ssh_content = """Host test
    HostName test.com
"""
    
    # 转换为YAML
    yaml_result = convert_ssh_config(ssh_content, to_yaml=True)
    assert "hosts:" in yaml_result
    
    # 转换为JSON  
    json_result = convert_ssh_config(ssh_content, to_json=True)
    assert '"Host": "test"' in json_result


if __name__ == "__main__":
    test_ssh_to_yaml()
    test_yaml_to_ssh()
    test_convert_function()
    print("All tests passed!")