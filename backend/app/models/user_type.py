"""
用户类型枚举
"""
from enum import Enum


class UserType(str, Enum):
    """
    用户类型枚举
    """
    STUDENT = "STUDENT"  # 学生
    TEACHER = "TEACHER"  # 教师
    ENTERPRISE = "ENTERPRISE"  # 企业
    ADMIN = "ADMIN"  # 管理员



