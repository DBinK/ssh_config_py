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

import os
import json
import yaml
from pathlib import Path
from typing import Union, Dict, List, Any, Optional

# 定义主机配置的类型
HostConfig = Dict[str, Union[str, List[str]]]

class SSHConfigConverter:
    """SSH配置文件转换器，支持SSH Config、YAML、JSON三种格式之间的相互转换"""
    
    @staticmethod
    def detect_format(content: str) -> str:
        """自动检测输入内容的格式"""
        content = content.strip()
        if not content:
            raise ValueError("Empty content")
            
        # 尝试JSON
        try:
            json.loads(content)
            return "json"
        except json.JSONDecodeError:
            pass
            
        # 尝试YAML
        try:
            yaml.safe_load(content)
            # 检查是否是有效的YAML结构（不是纯字符串）
            parsed = yaml.safe_load(content)
            if isinstance(parsed, (dict, list)):
                return "yaml"
        except yaml.YAMLError:
            pass
            
        # 默认为SSH Config格式
        return "ssh"
    
    @staticmethod
    def ssh_to_dict(content: str) -> Dict[str, Any]:
        """将SSH Config格式转换为字典"""
        hosts: List[HostConfig] = []
        current_host: Optional[HostConfig] = None
        lines = content.split('\n')
        
        # 多值选项列表
        multi_value_keys = {'identityfile', 'localforward', 'remoteforward'}
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            parts = line.split(maxsplit=1)
            if len(parts) < 2:
                continue
                
            key, value = parts[0].lower(), parts[1]
            
            if key == 'host':
                if current_host is not None:
                    hosts.append(current_host)
                current_host = {'Host': value}
            else:
                if current_host is None:
                    # 全局配置
                    if not hosts:
                        hosts.append({'Host': '*'})
                    current_host = hosts[0] if hosts[0]['Host'] == '*' else {'Host': '*'}
                    if current_host['Host'] != '*':
                        hosts.insert(0, {'Host': '*'})
                        current_host = hosts[0]
                
                # 处理多值选项（如IdentityFile）
                capitalized_key = key.capitalize()
                if key in multi_value_keys:
                    if capitalized_key not in current_host:
                        current_host[capitalized_key] = []
                    # 确保值是列表类型
                    current_host[capitalized_key] = current_host[capitalized_key]  # type: ignore
                    current_host[capitalized_key].append(value)  # type: ignore
                else:
                    current_host[capitalized_key] = value
        
        if current_host is not None:
            hosts.append(current_host)
            
        return {"hosts": hosts}
    
    @staticmethod
    def dict_to_ssh(data: Dict[str, Any]) -> str:
        """将字典转换为SSH Config格式"""
        if not isinstance(data, dict) or 'hosts' not in data:
            raise ValueError("Invalid data format for SSH conversion")
            
        lines = []
        for host in data['hosts']:
            if not isinstance(host, dict) or 'Host' not in host:
                continue
                
            lines.append(f"Host {host['Host']}")
            
            for key, value in host.items():
                if key == 'Host':
                    continue
                    
                if isinstance(value, list):
                    for item in value:
                        lines.append(f"    {key} {item}")
                else:
                    lines.append(f"    {key} {value}")
            lines.append("")  # 空行分隔
            
        return '\n'.join(lines).rstrip()
    
    @staticmethod
    def yaml_to_dict(content: str) -> Dict[str, Any]:
        """将YAML格式转换为字典"""
        return yaml.safe_load(content)
    
    @staticmethod
    def dict_to_yaml(data: Dict[str, Any]) -> str:
        """将字典转换为YAML格式"""
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)
    
    @staticmethod
    def json_to_dict(content: str) -> Dict[str, Any]:
        """将JSON格式转换为字典"""
        return json.loads(content)
    
    @staticmethod
    def dict_to_json(data: Dict[str, Any]) -> str:
        """将字典转换为JSON格式"""
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def convert(self, input_content: str, target_format: str) -> str:
        """转换内容到指定格式"""
        source_format = self.detect_format(input_content)
        
        if source_format == target_format:
            return input_content
            
        # 转换为中间字典格式
        if source_format == "ssh":
            data = self.ssh_to_dict(input_content)
        elif source_format == "yaml":
            data = self.yaml_to_dict(input_content)
        elif source_format == "json":
            data = self.json_to_dict(input_content)
        else:
            raise ValueError(f"Unsupported source format: {source_format}")
        
        # 转换为目标格式
        if target_format == "ssh":
            return self.dict_to_ssh(data)
        elif target_format == "yaml":
            return self.dict_to_yaml(data)
        elif target_format == "json":
            return self.dict_to_json(data)
        else:
            raise ValueError(f"Unsupported target format: {target_format}")


def convert_ssh_config(
    input_content: str, 
    to_yaml: bool = False, 
    to_json: bool = False, 
    to_ssh: bool = False
) -> str:
    """便捷函数：转换SSH配置内容
    
    Args:
        input_content: 输入内容
        to_yaml: 转换为YAML格式
        to_json: 转换为JSON格式  
        to_ssh: 转换为SSH Config格式
        
    Returns:
        转换后的内容字符串
    """
    converter = SSHConfigConverter()
    
    format_count = sum([to_yaml, to_json, to_ssh])
    if format_count != 1:
        raise ValueError("Exactly one output format must be specified")
        
    if to_yaml:
        return converter.convert(input_content, "yaml")
    elif to_json:
        return converter.convert(input_content, "json")
    elif to_ssh:
        return converter.convert(input_content, "ssh")
    else:
        # 默认转换为YAML
        return converter.convert(input_content, "yaml")