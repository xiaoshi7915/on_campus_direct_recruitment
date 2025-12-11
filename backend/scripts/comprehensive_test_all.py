"""
完整功能测试脚本
测试所有核心功能：审批流程、教师管理、子账号管理等
"""
import sys
import asyncio
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import httpx
from app.core.config import settings

BASE_URL = "http://localhost:5001"


async def test_all_features():
    """测试所有核心功能"""
    print("=" * 60)
    print("完整功能测试")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        results = []
        
        # ========== 1. 测试教师审批功能 ==========
        print("\n【1. 教师审批功能测试】")
        print("-" * 60)
        
        # 1.1 管理员登录
        print("\n1.1 管理员登录...")
        admin_login = await client.post(
            f"{BASE_URL}/api/v1/auth/login",
            data={"username": "admin", "password": "admin123"}
        )
        
        if admin_login.status_code != 200:
            print("⚠️  管理员登录失败，请先创建管理员账号")
            print("   可以使用以下命令创建：")
            print("   python scripts/create_test_data.py")
        else:
            admin_token = admin_login.json()["access_token"]
            admin_headers = {"Authorization": f"Bearer {admin_token}"}
            print("✅ 管理员登录成功")
            
            # 1.2 获取待审批教师列表
            print("\n1.2 获取待审批教师列表...")
            pending_teachers = await client.get(
                f"{BASE_URL}/api/v1/teacher-management/pending-approvals",
                headers=admin_headers
            )
            
            if pending_teachers.status_code == 200:
                teachers_data = pending_teachers.json()
                print(f"✅ 找到 {teachers_data.get('total', 0)} 个待审批教师")
                
                if teachers_data.get('items'):
                    teacher_id = teachers_data['items'][0]['id']
                    
                    # 1.3 审批教师
                    print(f"\n1.3 审批教师 {teacher_id}...")
                    approve_response = await client.post(
                        f"{BASE_URL}/api/v1/teacher-management/{teacher_id}/approve",
                        json={"action": "APPROVE", "comment": "测试审批通过"},
                        headers=admin_headers
                    )
                    
                    if approve_response.status_code == 200:
                        print("✅ 教师审批成功")
                        results.append(True)
                    else:
                        print(f"❌ 教师审批失败: {approve_response.text}")
                        results.append(False)
                else:
                    print("⚠️  没有待审批教师")
                    results.append(True)
            else:
                print(f"❌ 获取待审批教师列表失败: {pending_teachers.text}")
                results.append(False)
        
        # ========== 2. 测试双选会审批功能 ==========
        print("\n【2. 双选会审批功能测试】")
        print("-" * 60)
        
        # 2.1 教师登录
        print("\n2.1 教师登录...")
        teacher_login = await client.post(
            f"{BASE_URL}/api/v1/auth/login",
            data={"username": "main_teacher", "password": "teacher123"}
        )
        
        if teacher_login.status_code != 200:
            print("⚠️  教师登录失败，请先运行 create_test_data.py 创建测试数据")
            results.append(False)
        else:
            teacher_token = teacher_login.json()["access_token"]
            teacher_headers = {"Authorization": f"Bearer {teacher_token}"}
            print("✅ 教师登录成功")
            
            # 2.2 获取待审批双选会列表
            print("\n2.2 获取待审批双选会列表...")
            pending_job_fairs = await client.get(
                f"{BASE_URL}/api/v1/job-fairs?status=PENDING",
                headers=teacher_headers
            )
            
            if pending_job_fairs.status_code == 200:
                job_fairs_data = pending_job_fairs.json()
                print(f"✅ 找到 {job_fairs_data.get('total', 0)} 个待审批双选会")
                
                if job_fairs_data.get('items'):
                    job_fair_id = job_fairs_data['items'][0]['id']
                    
                    # 2.3 审批双选会
                    print(f"\n2.3 审批双选会 {job_fair_id}...")
                    approve_jf = await client.post(
                        f"{BASE_URL}/api/v1/approvals/job-fairs/{job_fair_id}/approve",
                        json={"action": "APPROVE", "comment": "测试审批通过"},
                        headers=teacher_headers
                    )
                    
                    if approve_jf.status_code == 200:
                        print("✅ 双选会审批成功")
                        results.append(True)
                    else:
                        print(f"❌ 双选会审批失败: {approve_jf.text}")
                        results.append(False)
                else:
                    print("⚠️  没有待审批双选会")
                    results.append(True)
            else:
                print(f"❌ 获取待审批双选会列表失败: {pending_job_fairs.text}")
                results.append(False)
        
        # ========== 3. 测试宣讲会审批功能 ==========
        print("\n【3. 宣讲会审批功能测试】")
        print("-" * 60)
        
        # 3.1 获取待审批宣讲会列表
        print("\n3.1 获取待审批宣讲会列表...")
        pending_sessions = await client.get(
            f"{BASE_URL}/api/v1/info-sessions?status=PENDING",
            headers=teacher_headers if teacher_login.status_code == 200 else {}
        )
        
        if pending_sessions.status_code == 200:
            sessions_data = pending_sessions.json()
            print(f"✅ 找到 {sessions_data.get('total', 0)} 个待审批宣讲会")
            
            if sessions_data.get('items'):
                session_id = sessions_data['items'][0]['id']
                
                # 3.2 审批宣讲会
                print(f"\n3.2 审批宣讲会 {session_id}...")
                approve_session = await client.post(
                    f"{BASE_URL}/api/v1/approvals/info-sessions/{session_id}/approve",
                    json={"action": "APPROVE", "comment": "测试审批通过"},
                    headers=teacher_headers if teacher_login.status_code == 200 else {}
                )
                
                if approve_session.status_code == 200:
                    print("✅ 宣讲会审批成功")
                    results.append(True)
                else:
                    print(f"❌ 宣讲会审批失败: {approve_session.text}")
                    results.append(False)
            else:
                print("⚠️  没有待审批宣讲会")
                results.append(True)
        else:
            print(f"❌ 获取待审批宣讲会列表失败: {pending_sessions.text}")
            results.append(False)
        
        # ========== 4. 测试子账号管理功能 ==========
        print("\n【4. 子账号管理功能测试】")
        print("-" * 60)
        
        if teacher_login.status_code == 200:
            # 4.1 获取子账号列表
            print("\n4.1 获取子账号列表...")
            sub_accounts = await client.get(
                f"{BASE_URL}/api/v1/teacher-management/sub-accounts",
                headers=teacher_headers
            )
            
            if sub_accounts.status_code == 200:
                sub_accounts_data = sub_accounts.json()
                print(f"✅ 找到 {sub_accounts_data.get('total', 0)} 个子账号")
                results.append(True)
            elif sub_accounts.status_code == 403:
                print("⚠️  当前账号不是主账号，无法查看子账号")
                results.append(True)
            else:
                print(f"❌ 获取子账号列表失败: {sub_accounts.text}")
                results.append(False)
            
            # 4.2 创建子账号
            print("\n4.2 创建子账号...")
            create_sub = await client.post(
                f"{BASE_URL}/api/v1/teacher-management/sub-accounts",
                json={
                    "username": f"sub_teacher_{asyncio.get_event_loop().time()}",
                    "password": "sub123456",
                    "real_name": "子账号教师",
                    "phone": "13800000999",
                    "title": "助教"
                },
                headers=teacher_headers
            )
            
            if create_sub.status_code == 201:
                print("✅ 创建子账号成功")
                results.append(True)
            elif create_sub.status_code == 403:
                print("⚠️  当前账号不是主账号，无法创建子账号")
                results.append(True)
            else:
                print(f"❌ 创建子账号失败: {create_sub.text}")
                results.append(False)
        else:
            print("⚠️  需要教师登录才能测试子账号管理")
            results.append(False)
        
        # ========== 5. 测试学校信息获取 ==========
        print("\n【5. 学校信息获取测试】")
        print("-" * 60)
        
        if teacher_login.status_code == 200:
            print("\n5.1 获取我的学校信息...")
            my_school = await client.get(
                f"{BASE_URL}/api/v1/schools/my-school",
                headers=teacher_headers
            )
            
            if my_school.status_code == 200:
                school_data = my_school.json()
                print(f"✅ 获取学校信息成功: {school_data.get('name')}")
                results.append(True)
            else:
                print(f"❌ 获取学校信息失败: {my_school.text}")
                results.append(False)
        else:
            print("⚠️  需要教师登录才能测试学校信息获取")
            results.append(False)
        
        # ========== 汇总结果 ==========
        print("\n" + "=" * 60)
        print("测试结果汇总")
        print("=" * 60)
        passed = sum(results)
        total = len(results)
        print(f"总测试数: {total}")
        print(f"通过: {passed} ✅")
        print(f"失败: {total - passed} ❌")
        print(f"通过率: {passed / total * 100:.1f}%")
        
        if passed == total:
            print("\n✅ 所有测试通过！")
        else:
            print("\n⚠️  部分测试未通过，请检查日志")
        
        return passed == total


if __name__ == "__main__":
    try:
        success = asyncio.run(test_all_features())
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 测试执行失败: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)



