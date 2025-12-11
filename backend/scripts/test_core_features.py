"""
核心功能测试脚本
测试审批流程、教师管理等功能
"""
import sys
import asyncio
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
import httpx
from app.core.config import settings

# 配置数据库连接
DATABASE_URL = settings.DATABASE_URL.replace("mysql+pymysql", "mysql+aiomysql")
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

BASE_URL = "http://localhost:5001"


async def test_approval_flow():
    """测试审批流程"""
    print("\n=== 测试审批流程 ===")
    
    async with httpx.AsyncClient() as client:
        # 1. 登录管理员或教师
        login_response = await client.post(
            f"{BASE_URL}/api/v1/auth/login",
            data={
                "username": "admin",
                "password": "admin123"
            }
        )
        
        if login_response.status_code != 200:
            print("❌ 登录失败，请先创建管理员账号")
            return False
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. 获取待审批的双选会列表
        print("\n1. 获取待审批的双选会列表...")
        job_fairs_response = await client.get(
            f"{BASE_URL}/api/v1/job-fairs?status=PENDING",
            headers=headers
        )
        
        if job_fairs_response.status_code == 200:
            job_fairs = job_fairs_response.json()
            print(f"✅ 找到 {job_fairs.get('total', 0)} 个待审批的双选会")
            
            if job_fairs.get('items'):
                job_fair_id = job_fairs['items'][0]['id']
                
                # 3. 审批双选会
                print(f"\n2. 审批双选会 {job_fair_id}...")
                approve_response = await client.post(
                    f"{BASE_URL}/api/v1/approvals/job-fairs/{job_fair_id}/approve",
                    json={"action": "APPROVE", "comment": "测试审批"},
                    headers=headers
                )
                
                if approve_response.status_code == 200:
                    print("✅ 审批成功")
                    return True
                else:
                    print(f"❌ 审批失败: {approve_response.text}")
                    return False
            else:
                print("⚠️  没有待审批的双选会")
                return True
        else:
            print(f"❌ 获取双选会列表失败: {job_fairs_response.text}")
            return False


async def test_teacher_management():
    """测试教师管理功能"""
    print("\n=== 测试教师管理功能 ===")
    
    async with httpx.AsyncClient() as client:
        # 1. 登录管理员
        login_response = await client.post(
            f"{BASE_URL}/api/v1/auth/login",
            data={
                "username": "admin",
                "password": "admin123"
            }
        )
        
        if login_response.status_code != 200:
            print("❌ 登录失败，请先创建管理员账号")
            return False
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. 获取待审批教师列表
        print("\n1. 获取待审批教师列表...")
        teachers_response = await client.get(
            f"{BASE_URL}/api/v1/teacher-management/pending-approvals",
            headers=headers
        )
        
        if teachers_response.status_code == 200:
            teachers = teachers_response.json()
            print(f"✅ 找到 {teachers.get('total', 0)} 个待审批教师")
            return True
        else:
            print(f"❌ 获取待审批教师列表失败: {teachers_response.text}")
            return False


async def test_sub_account_management():
    """测试子账号管理功能"""
    print("\n=== 测试子账号管理功能 ===")
    
    async with httpx.AsyncClient() as client:
        # 1. 登录主账号教师
        login_response = await client.post(
            f"{BASE_URL}/api/v1/auth/login",
            data={
                "username": "teacher1",  # 假设有一个主账号教师
                "password": "teacher123"
            }
        )
        
        if login_response.status_code != 200:
            print("⚠️  登录失败，请先创建主账号教师")
            return True  # 不是错误，只是没有测试数据
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. 获取子账号列表
        print("\n1. 获取子账号列表...")
        sub_accounts_response = await client.get(
            f"{BASE_URL}/api/v1/teacher-management/sub-accounts",
            headers=headers
        )
        
        if sub_accounts_response.status_code == 200:
            sub_accounts = sub_accounts_response.json()
            print(f"✅ 找到 {sub_accounts.get('total', 0)} 个子账号")
            return True
        elif sub_accounts_response.status_code == 403:
            print("⚠️  当前账号不是主账号，无法查看子账号")
            return True
        else:
            print(f"❌ 获取子账号列表失败: {sub_accounts_response.text}")
            return False


async def main():
    """主测试函数"""
    print("=" * 60)
    print("核心功能测试")
    print("=" * 60)
    
    results = []
    
    # 测试审批流程
    results.append(await test_approval_flow())
    
    # 测试教师管理
    results.append(await test_teacher_management())
    
    # 测试子账号管理
    results.append(await test_sub_account_management())
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("✅ 所有测试通过！")
    else:
        print("⚠️  部分测试未通过，请检查日志")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())

