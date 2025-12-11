"""
认证相关的Pydantic模式
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Union


class RegisterRequest(BaseModel):
    """
    注册请求模式
    """
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, max_length=100, description="密码")
    phone: Optional[str] = Field(None, description="手机号")
    email: Optional[str] = Field(None, description="邮箱")
    user_type: str = Field(..., description="用户类型：STUDENT, TEACHER, ENTERPRISE, ADMIN")
    
    @field_validator('email', mode='before')
    @classmethod
    def validate_email(cls, v: Union[str, None]) -> Optional[str]:
        """验证邮箱格式，如果为空字符串则返回None"""
        if not v or (isinstance(v, str) and v.strip() == ''):
            return None
        # 简单的邮箱格式验证
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('邮箱格式不正确')
        return v
    
    @field_validator('phone', mode='before')
    @classmethod
    def validate_phone(cls, v: Union[str, None]) -> Optional[str]:
        """验证手机号格式，如果为空字符串则返回None"""
        if not v or (isinstance(v, str) and v.strip() == ''):
            return None
        # 简单的手机号格式验证
        import re
        phone_pattern = r'^1[3-9]\d{9}$'
        if not re.match(phone_pattern, v):
            raise ValueError('手机号格式不正确')
        return v


class LoginResponse(BaseModel):
    """
    登录响应模式
    """
    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    token_type: str = Field(default="bearer", description="令牌类型")


class TokenResponse(BaseModel):
    """
    令牌响应模式
    """
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")


