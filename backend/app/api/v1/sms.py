"""
短信验证码API
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from app.services.sms import send_sms_code, verify_sms_code
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


class SendSMSRequest(BaseModel):
    """发送短信验证码请求"""
    phone: str = Field(..., description="手机号", pattern=r"^1[3-9]\d{9}$")


class VerifySMSRequest(BaseModel):
    """验证短信验证码请求"""
    phone: str = Field(..., description="手机号", pattern=r"^1[3-9]\d{9}$")
    code: str = Field(..., description="验证码", min_length=6, max_length=6)


@router.post("/send")
async def send_sms(
    request: SendSMSRequest
):
    """
    发送短信验证码
    
    Args:
        request: 发送短信请求
        
    Returns:
        发送结果（开发环境返回验证码）
    """
    try:
        code = await send_sms_code(request.phone)
        
        # 开发环境返回验证码，方便测试
        from app.core.config import settings
        if settings.DEBUG and code:
            return {
                "success": True,
                "message": "验证码已发送（开发模式）",
                "code": code  # 仅开发环境返回
            }
        
        return {
            "success": True,
            "message": "验证码已发送"
        }
        
    except Exception as e:
        logger.error(f"发送短信验证码失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="发送验证码失败，请稍后重试"
        )


@router.post("/verify")
async def verify_sms(
    request: VerifySMSRequest
):
    """
    验证短信验证码
    
    Args:
        request: 验证短信请求
        
    Returns:
        验证结果
    """
    try:
        is_valid = await verify_sms_code(request.phone, request.code)
        
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码错误或已过期"
            )
        
        return {
            "success": True,
            "message": "验证码验证成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"验证短信验证码失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="验证失败，请稍后重试"
        )

