"""
时间处理工具模块
统一使用UTC时间，避免时区问题
"""
from datetime import datetime, timezone
from typing import Optional


def utc_now() -> datetime:
    """
    获取当前UTC时间
    
    Returns:
        datetime: 当前UTC时间
    """
    return datetime.now(timezone.utc)


def to_utc(dt: Optional[datetime]) -> Optional[datetime]:
    """
    将datetime转换为UTC时间（如果已经是UTC则返回原值）
    
    Args:
        dt: 要转换的datetime对象
        
    Returns:
        datetime: UTC时间，如果输入为None则返回None
    """
    if dt is None:
        return None
    
    # 如果已经有timezone信息
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc)
    
    # 如果没有timezone信息，假设是本地时间并转换为UTC
    # 注意：这需要根据实际情况调整
    return dt.replace(tzinfo=timezone.utc)


def format_datetime(dt: Optional[datetime], format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[str]:
    """
    格式化datetime为字符串
    
    Args:
        dt: datetime对象
        format_str: 格式化字符串
        
    Returns:
        str: 格式化后的字符串，如果输入为None则返回None
    """
    if dt is None:
        return None
    return dt.strftime(format_str)


def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """
    解析字符串为datetime对象（UTC）
    
    Args:
        dt_str: 日期时间字符串
        format_str: 格式化字符串
        
    Returns:
        datetime: UTC时间对象
    """
    dt = datetime.strptime(dt_str, format_str)
    return dt.replace(tzinfo=timezone.utc)


