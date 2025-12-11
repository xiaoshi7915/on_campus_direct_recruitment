"""
测试短信服务功能（开发模式）
"""
import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.sms import send_sms_code, verify_sms_code
from app.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


async def test_sms_service():
    """测试短信服务"""
    print("=" * 60)
    print("短信服务功能测试（开发模式）")
    print("=" * 60)
    
    # 测试手机号
    test_phone = "13800138000"
    
    # 1. 测试发送验证码
    print(f"\n1. 测试发送验证码到 {test_phone}...")
    try:
        code = await send_sms_code(test_phone)
        if code:
            print(f"[OK] 验证码发送成功！验证码: {code}")
        else:
            print("[ERROR] 验证码发送失败（返回None）")
            return
    except Exception as e:
        print(f"[ERROR] 发送验证码时出错: {str(e)}")
        return
    
    # 等待一下
    await asyncio.sleep(1)
    
    # 2. 测试验证正确的验证码
    print(f"\n2. 测试验证正确的验证码: {code}...")
    try:
        result = await verify_sms_code(test_phone, code)
        if result:
            print("[OK] 验证码验证成功！")
        else:
            print("[ERROR] 验证码验证失败")
    except Exception as e:
        print(f"[ERROR] 验证验证码时出错: {str(e)}")
    
    # 3. 测试验证错误的验证码
    print(f"\n3. 测试验证错误的验证码: 000000...")
    try:
        result = await verify_sms_code(test_phone, "000000")
        if not result:
            print("[OK] 错误验证码被正确拒绝")
        else:
            print("[ERROR] 错误验证码被错误接受")
    except Exception as e:
        print(f"[ERROR] 验证验证码时出错: {str(e)}")
    
    # 4. 测试验证已使用的验证码（一次性使用）
    print(f"\n4. 测试验证已使用的验证码（一次性使用）...")
    try:
        # 重新发送验证码
        new_code = await send_sms_code(test_phone)
        if new_code:
            # 先验证一次（应该成功）
            result1 = await verify_sms_code(test_phone, new_code)
            if result1:
                print(f"[OK] 第一次验证成功（验证码: {new_code}）")
            else:
                print("[ERROR] 第一次验证失败")
                return
            
            # 再次验证同一个验证码（应该失败）
            result2 = await verify_sms_code(test_phone, new_code)
            if not result2:
                print("[OK] 已使用的验证码被正确拒绝（一次性使用）")
            else:
                print("[ERROR] 已使用的验证码被错误接受")
        else:
            print("[ERROR] 重新发送验证码失败")
    except Exception as e:
        print(f"[ERROR] 测试一次性使用时出错: {str(e)}")
    
    # 5. 测试验证不存在的手机号
    print(f"\n5. 测试验证不存在的手机号: 13999999999...")
    try:
        result = await verify_sms_code("13999999999", "123456")
        if not result:
            print("[OK] 不存在的手机号被正确拒绝")
        else:
            print("[ERROR] 不存在的手机号被错误接受")
    except Exception as e:
        print(f"[ERROR] 测试不存在手机号时出错: {str(e)}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


async def test_sms_api():
    """测试短信API（需要后端服务运行）"""
    print("\n" + "=" * 60)
    print("短信API测试（需要后端服务运行在 http://localhost:5001）")
    print("=" * 60)
    
    import httpx
    
    test_phone = "13800138000"
    
    async with httpx.AsyncClient(base_url="http://localhost:5001") as client:
        # 1. 发送验证码
        print(f"\n1. 发送验证码到 {test_phone}...")
        try:
            response = await client.post(
                "/api/v1/sms/send",
                json={"phone": test_phone}
            )
            print(f"状态码: {response.status_code}")
            data = response.json()
            print(f"响应: {data}")
            
            if response.status_code == 200 and data.get("success"):
                code = data.get("code")
                if code:
                    print(f"[OK] 验证码发送成功！验证码: {code}")
                    
                    # 2. 验证正确的验证码
                    print(f"\n2. 验证正确的验证码: {code}...")
                    verify_response = await client.post(
                        "/api/v1/sms/verify",
                        json={"phone": test_phone, "code": code}
                    )
                    print(f"状态码: {verify_response.status_code}")
                    verify_data = verify_response.json()
                    print(f"响应: {verify_data}")
                    
                    if verify_response.status_code == 200 and verify_data.get("success"):
                        print("[OK] 验证码验证成功！")
                    else:
                        print("[ERROR] 验证码验证失败")
                    
                    # 3. 验证错误的验证码
                    print(f"\n3. 验证错误的验证码: 000000...")
                    error_response = await client.post(
                        "/api/v1/sms/verify",
                        json={"phone": test_phone, "code": "000000"}
                    )
                    print(f"状态码: {error_response.status_code}")
                    error_data = error_response.json()
                    print(f"响应: {error_data}")
                    
                    if error_response.status_code == 400:
                        print("[OK] 错误验证码被正确拒绝")
                    else:
                        print("[ERROR] 错误验证码未被正确拒绝")
                else:
                    print("[WARN] 开发模式应返回验证码，但未返回")
            else:
                print("[ERROR] 发送验证码失败")
        except httpx.ConnectError:
            print("[ERROR] 无法连接到后端服务，请确保后端服务运行在 http://localhost:5001")
        except Exception as e:
            print(f"[ERROR] 测试API时出错: {str(e)}")


async def main():
    """主函数"""
    # 测试服务层
    await test_sms_service()
    
    # 测试API层（可选）
    print("\n是否测试API层？(需要后端服务运行)")
    print("提示：如果后端服务未运行，API测试将跳过")
    try:
        await test_sms_api()
    except Exception as e:
        print(f"\n⚠️ API测试跳过: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())

