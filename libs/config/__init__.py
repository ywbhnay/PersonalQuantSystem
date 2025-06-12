#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
包含配置管理器和常量定义
"""

from .config_manager import ConfigManager
from .consts import *

__all__ = [
    'ConfigManager',
    # 从consts导入的常量
]