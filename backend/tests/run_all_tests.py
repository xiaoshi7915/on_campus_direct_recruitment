"""
运行所有测试的脚本
"""
import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """运行所有测试"""
    # 测试文件列表
    test_files = [
        "test_database_session.py",
        "test_websocket_auth.py",
        "test_redis_pool.py",
        "test_rate_limiting.py",
        "test_n_plus_one_query.py",
        "test_exception_handling.py",
    ]
    
    # 运行测试
    test_paths = [os.path.join(os.path.dirname(__file__), f) for f in test_files]
    
    # 执行pytest
    exit_code = pytest.main([
        "-v",  # 详细输出
        "--tb=short",  # 简短的错误追踪
        "--color=yes",  # 彩色输出
        *test_paths
    ])
    
    return exit_code

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

