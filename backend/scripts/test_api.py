"""
API接口测试脚本
测试所有API接口的功能
"""
import asyncio
import sys
import os
import httpx
from typing import Dict, Any

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:5001"
API_BASE = f"{BASE_URL}/api/v1"

# 测试结果
test_results = {
    "passed": [],
    "failed": [],
    "skipped": []
}


async def test_endpoint(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    name: str,
    headers: Dict[str, str] = None,
    json: Dict[str, Any] = None,
    expected_status: int = 200
):
    """测试API端点"""
    try:
        if method.upper() == "GET":
            response = await client.get(url, headers=headers)
        elif method.upper() == "POST":
            response = await client.post(url, headers=headers, json=json)
        elif method.upper() == "PUT":
            response = await client.put(url, headers=headers, json=json)
        elif method.upper() == "DELETE":
            response = await client.delete(url, headers=headers)
        else:
            test_results["skipped"].append(f"{name} - 不支持的HTTP方法: {method}")
            return
        
        if response.status_code == expected_status:
            test_results["passed"].append(f"{name} - {method} {url}")
            print(f"[PASS] {name}")
        else:
            test_results["failed"].append(
                f"{name} - {method} {url} - 期望状态码: {expected_status}, 实际: {response.status_code}"
            )
            print(f"[FAIL] {name} - 状态码: {response.status_code}, 响应: {response.text[:200]}")
    except Exception as e:
        test_results["failed"].append(f"{name} - {method} {url} - 错误: {str(e)}")
        print(f"[FAIL] {name} - 错误: {str(e)}")


async def main():
    """主测试函数"""
    print("=" * 60)
    print("开始测试API接口...")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. 测试认证相关API
        print("\n1. 测试认证相关API...")
        
        # 注册用户
        import random
        username = f"testuser{random.randint(1000, 9999)}"
        register_data = {
            "username": username,
            "password": "123456",
            "phone": f"138{random.randint(10000000, 99999999)}",
            "email": f"{username}@example.com",
            "user_type": "STUDENT"
        }
        register_response = await client.post(f"{API_BASE}/auth/register", json=register_data)
        if register_response.status_code == 201:
            test_results["passed"].append("用户注册")
            print("[PASS] 用户注册")
        else:
            test_results["failed"].append(f"用户注册 - 状态码: {register_response.status_code}, 响应: {register_response.text[:200]}")
            print(f"[FAIL] 用户注册 - 状态码: {register_response.status_code}, 响应: {register_response.text[:200]}")
        
        # 登录（OAuth2使用form data）
        login_response = await client.post(
            f"{API_BASE}/auth/login",
            data={"username": username, "password": "123456"}  # OAuth2使用form data
        )
        token = None
        if login_response.status_code == 200:
            data = login_response.json()
            token = data.get("access_token")
            test_results["passed"].append("用户登录")
            print("[PASS] 用户登录")
        else:
            test_results["failed"].append(f"用户登录 - 状态码: {login_response.status_code}, 响应: {login_response.text[:200]}")
            print(f"[FAIL] 用户登录 - 状态码: {login_response.status_code}, 响应: {login_response.text[:200]}")
        
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        
        # 2. 测试用户相关API
        print("\n2. 测试用户相关API...")
        await test_endpoint(client, "GET", f"{API_BASE}/users/me", "获取当前用户信息", headers=headers)
        
        # 3. 测试职位相关API
        print("\n3. 测试职位相关API...")
        await test_endpoint(client, "GET", f"{API_BASE}/jobs", "获取职位列表", headers=headers)
        await test_endpoint(client, "GET", f"{API_BASE}/jobs?page=1&page_size=10", "获取职位列表（分页）", headers=headers)
        
        # 4. 测试简历相关API
        print("\n4. 测试简历相关API...")
        await test_endpoint(client, "GET", f"{API_BASE}/resumes", "获取简历列表", headers=headers)
        
        # 5. 测试职位申请API
        print("\n5. 测试职位申请API...")
        await test_endpoint(client, "GET", f"{API_BASE}/applications", "获取申请列表", headers=headers)
        
        # 6. 测试双选会API
        print("\n6. 测试双选会API...")
        await test_endpoint(client, "GET", f"{API_BASE}/job-fairs", "获取双选会列表", headers=headers)
        
        # 7. 测试宣讲会API
        print("\n7. 测试宣讲会API...")
        await test_endpoint(client, "GET", f"{API_BASE}/info-sessions", "获取宣讲会列表", headers=headers)
        
        # 8. 测试面试API
        print("\n8. 测试面试API...")
        await test_endpoint(client, "GET", f"{API_BASE}/interviews", "获取面试列表", headers=headers)
        
        # 9. 测试日程API
        print("\n9. 测试日程API...")
        await test_endpoint(client, "GET", f"{API_BASE}/schedules", "获取日程列表", headers=headers)
        
        # 10. 测试收藏API
        print("\n10. 测试收藏API...")
        await test_endpoint(client, "GET", f"{API_BASE}/favorites", "获取收藏列表", headers=headers)
        
        # 11. 测试聊天API
        print("\n11. 测试聊天API...")
        await test_endpoint(client, "GET", f"{API_BASE}/chat/sessions", "获取聊天会话列表", headers=headers)
        
        # 12. 测试数据统计API
        print("\n12. 测试数据统计API...")
        await test_endpoint(client, "GET", f"{API_BASE}/statistics/platform/overview", "获取平台概览统计", headers=headers, expected_status=403)  # 需要管理员权限
        
        # 13. 测试API文档
        print("\n13. 测试API文档...")
        await test_endpoint(client, "GET", f"{BASE_URL}/docs", "API文档页面", expected_status=200)
        await test_endpoint(client, "GET", f"{BASE_URL}/openapi.json", "OpenAPI规范", expected_status=200)
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    print(f"通过: {len(test_results['passed'])}")
    print(f"失败: {len(test_results['failed'])}")
    print(f"跳过: {len(test_results['skipped'])}")
    
    if test_results['failed']:
        print("\n失败的测试:")
        for failure in test_results['failed']:
            print(f"  - {failure}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
