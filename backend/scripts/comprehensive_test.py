"""
前后端全面测试脚本
"""
import asyncio
import httpx
import json
from typing import Dict, Any

BASE_URL = "http://localhost:5001/api/v1"

# 测试结果统计
test_results = {
    "passed": 0,
    "failed": 0,
    "total": 0,
    "errors": []
}


async def test_api(
    client: httpx.AsyncClient,
    method: str,
    endpoint: str,
    name: str,
    data: Dict = None,
    headers: Dict = None,
    expected_status: int = 200
) -> bool:
    """测试API接口"""
    test_results["total"] += 1
    try:
        url = f"{BASE_URL}{endpoint}"
        response = await client.request(
            method=method,
            url=url,
            json=data,
            headers=headers,
            timeout=10.0
        )
        
        if response.status_code == expected_status:
            test_results["passed"] += 1
            print(f"✅ {name}")
            return True
        else:
            test_results["failed"] += 1
            error_msg = f"❌ {name}: 期望状态码 {expected_status}, 实际 {response.status_code}"
            print(error_msg)
            test_results["errors"].append(error_msg)
            return False
    except Exception as e:
        test_results["failed"] += 1
        error_msg = f"❌ {name}: {str(e)}"
        print(error_msg)
        test_results["errors"].append(error_msg)
        return False


async def main():
    """主测试函数"""
    print("=" * 60)
    print("开始全面API测试")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        # 1. 健康检查
        print("\n【1. 健康检查】")
        await test_api(client, "GET", "/health", "健康检查", expected_status=200)
        
        # 2. 用户注册
        print("\n【2. 用户认证】")
        register_data = {
            "username": "test_student",
            "password": "123456",
            "user_type": "STUDENT",
            "phone": "13800138000",
            "email": "test@example.com"
        }
        await test_api(client, "POST", "/auth/register", "用户注册", data=register_data)
        
        # 3. 用户登录
        login_data = {
            "username": "test_student",
            "password": "123456"
        }
        login_response = await client.post(
            f"{BASE_URL}/auth/login",
            data=login_data,
            timeout=10.0
        )
        
        token = None
        if login_response.status_code == 200:
            result = login_response.json()
            token = result.get("access_token")
            print(f"✅ 用户登录 (token: {token[:20]}...)")
            test_results["passed"] += 1
            test_results["total"] += 1
        else:
            print(f"❌ 用户登录: {login_response.status_code}")
            test_results["failed"] += 1
            test_results["total"] += 1
        
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        
        # 4. 获取当前用户信息
        print("\n【3. 用户信息】")
        await test_api(client, "GET", "/users/me", "获取当前用户信息", headers=headers)
        
        # 5. 职位相关API
        print("\n【4. 职位管理】")
        await test_api(client, "GET", "/jobs?page=1&page_size=10", "获取职位列表")
        await test_api(client, "GET", "/jobs?page=1&page_size=10", "获取职位列表（带认证）", headers=headers)
        
        # 6. 简历相关API
        print("\n【5. 简历管理】")
        await test_api(client, "GET", "/resumes", "获取简历列表", headers=headers)
        
        # 7. 申请相关API
        print("\n【6. 申请管理】")
        await test_api(client, "GET", "/applications", "获取申请列表", headers=headers)
        
        # 8. 双选会相关API
        print("\n【7. 双选会管理】")
        await test_api(client, "GET", "/job-fairs?page=1&page_size=10", "获取双选会列表")
        
        # 9. 宣讲会相关API
        print("\n【8. 宣讲会管理】")
        await test_api(client, "GET", "/info-sessions?page=1&page_size=10", "获取宣讲会列表")
        
        # 10. 面试相关API
        print("\n【9. 面试管理】")
        await test_api(client, "GET", "/interviews", "获取面试列表", headers=headers)
        
        # 11. 日程相关API
        print("\n【10. 日程管理】")
        await test_api(client, "GET", "/schedules", "获取日程列表", headers=headers)
        
        # 12. 收藏相关API
        print("\n【11. 收藏管理】")
        await test_api(client, "GET", "/favorites", "获取收藏列表", headers=headers)
        
        # 13. 统计相关API
        print("\n【12. 数据统计】")
        # 需要教师或管理员权限，这里只测试接口是否存在
        await test_api(client, "GET", "/statistics/students/activity", "学生活跃度统计", headers=headers, expected_status=403)
        
        # 14. 文件上传相关API
        print("\n【13. 文件上传】")
        # 文件上传需要multipart/form-data，这里只测试接口是否存在
        await test_api(client, "GET", "/upload", "文件上传接口", headers=headers, expected_status=405)
        
    # 打印测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    print(f"总测试数: {test_results['total']}")
    print(f"通过: {test_results['passed']} ✅")
    print(f"失败: {test_results['failed']} ❌")
    print(f"通过率: {test_results['passed'] / test_results['total'] * 100:.1f}%")
    
    if test_results['errors']:
        print("\n错误详情:")
        for error in test_results['errors']:
            print(f"  - {error}")
    
    print("=" * 60)
    
    return test_results['failed'] == 0


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)


