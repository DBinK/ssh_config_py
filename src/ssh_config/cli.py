# Copyright 2025 Your Name
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

"""Command-line interface for SSH Config Tool."""

import sys
import os
import argparse
from pathlib import Path
from typing import Optional

from .core import convert_ssh_config


def is_stdin_piped() -> bool:
    """检查是否从标准输入读取"""
    return not sys.stdin.isatty()


def read_input_content(src: Optional[str] = None) -> str:
    """读取输入内容"""
    if is_stdin_piped():
        return sys.stdin.read()
    
    if src is None:
        # 默认读取 ~/.ssh 目录
        ssh_dir = Path.home() / ".ssh"
        if not ssh_dir.exists():
            raise FileNotFoundError(f"SSH directory not found: {ssh_dir}")
        
        # 查找配置文件
        config_files = []
        for file_path in ssh_dir.iterdir():
            if file_path.is_file() and file_path.name not in ['id_rsa', 'id_rsa.pub', 'known_hosts']:
                if file_path.suffix not in ['.pub', '.pem', '.key']:
                    config_files.append(file_path)
        
        if not config_files:
            raise FileNotFoundError("No SSH config files found in ~/.ssh")
            
        # 读取第一个配置文件或合并所有
        content = ""
        for config_file in sorted(config_files):
            if config_file.name == 'config':
                with open(config_file, 'r') as f:
                    content = f.read()
                break
        else:
            # 如果没有config文件，读取第一个找到的文件
            with open(config_files[0], 'r') as f:
                content = f.read()
                
        return content
    
    # 从指定文件读取
    src_path = Path(src)
    if not src_path.exists():
        raise FileNotFoundError(f"Source file not found: {src}")
    
    with open(src_path, 'r') as f:
        return f.read()


def write_output_content(content: str, dest: Optional[str] = None):
    """写入输出内容"""
    if dest is None or is_stdin_piped():
        print(content)
        return
    
    dest_path = Path(dest)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(dest_path, 'w') as f:
        f.write(content)
    
    print(f"File has been saved successfully")
    print(f"File path: {dest_path}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="SSH Config Tool - Convert between SSH config, YAML, and JSON formats"
    )
    parser.add_argument(
        "--to-yaml", 
        action="store_true", 
        help="Convert SSH config(Text/JSON) to YAML"
    )
    parser.add_argument(
        "--to-ssh", 
        action="store_true", 
        help="Convert SSH config(YAML/JSON) to SSH config format"
    )
    parser.add_argument(
        "--to-json", 
        action="store_true", 
        help="Convert SSH config(YAML/Text) to JSON"
    )
    parser.add_argument(
        "--src", 
        type=str, 
        help="Source file or directories path, valid when using non-pipeline mode"
    )
    parser.add_argument(
        "--dest", 
        type=str, 
        help="Destination file path, valid when using non-pipeline mode"
    )
    parser.add_argument(
        "--help", 
        action="help", 
        help="Show this help message"
    )
    
    args = parser.parse_args()
    
    # 验证转换参数
    format_count = sum([args.to_yaml, args.to_ssh, args.to_json])
    if format_count != 1:
        print("Please specify either --to-yaml or --to-ssh or --to-json")
        sys.exit(1)
    
    try:
        # 读取输入
        input_content = read_input_content(args.src)
        
        # 执行转换
        output_content = convert_ssh_config(
            input_content,
            to_yaml=args.to_yaml,
            to_json=args.to_json,
            to_ssh=args.to_ssh
        )
        
        # 写入输出
        write_output_content(output_content, args.dest)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()