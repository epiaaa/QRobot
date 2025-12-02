import os
import sys

import yaml


def get_root_path() -> str:
    """
    动态定位项目根目录（基于 requirements.txt 的位置）
    """
    # 当前文件（path_utils.py）的绝对路径
    current_path = os.path.abspath(__file__)

    # 向上遍历目录，直到找到包含 pyproject.toml 的目录（即项目根）
    while True:
        # 检查当前目录是否包含项目标识文件
        if os.path.exists(os.path.join(current_path, "requirements.txt")):
            return current_path

        # 向上移动一级目录
        parent_path = os.path.dirname(current_path)

        # 防止无限循环（到达系统根目录仍未找到）
        if parent_path == current_path:
            raise FileNotFoundError("未找到项目根目录（缺少 pyproject.toml）")

        current_path = parent_path


def add_root_to_sys_path(path: str = None) -> None:
    """
    将项目根目录添加到 sys.path（确保模块可被导入）
    """
    if path:
        root = path
    else:
        root = get_root_path()
    if root in sys.path:
        sys.path.remove(root)
    sys.path.insert(0, root)  # 插入到最前面，优先搜索根目录


def json_to_class(file, class_):
    """将JSON文件转换为类"""
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return class_.model_validate_json(f.read())
    raise FileNotFoundError(f"{file} 不存在")


def additional_text(path, content):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(path, "a", encoding="utf-8") as f:
        f.write(content+"\n")

