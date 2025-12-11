"""
短信验证码服务
支持阿里云短信服务
"""
import random
import asyncio
import json
from typing import Optional
from app.core.config import settings
from app.core.logging import get_logger
from app.core.cache import set_cache, get_cache, delete_cache

logger = get_logger(__name__)

# 简单的内存验证码存储（生产环境应使用Redis）
sms_codes = {}


async def send_sms_code(phone: str) -> Optional[str]:
    """
    发送短信验证码
    
    Args:
        phone: 手机号
        
    Returns:
        验证码（开发环境返回，生产环境不返回）
    """
    # 生成6位数字验证码
    code = str(random.randint(100000, 999999))
    
    # 如果配置了阿里云短信服务，使用真实服务
    if settings.SMS_ACCESS_KEY_ID and settings.SMS_ACCESS_KEY_SECRET:
        try:
            # 使用阿里云短信服务SDK
            from aliyunsdkcore.client import AcsClient
            from aliyunsdkcore.request import CommonRequest
            
            # 创建AcsClient实例
            client = AcsClient(
                settings.SMS_ACCESS_KEY_ID,
                settings.SMS_ACCESS_KEY_SECRET,
                "cn-hangzhou"  # 短信服务区域，可根据实际情况调整
            )
            
            # 创建请求对象
            request = CommonRequest()
            request.set_accept_format('json')
            request.set_domain('dysmsapi.aliyuncs.com')
            request.set_method('POST')
            request.set_protocol_type('https')
            request.set_version('2017-05-25')
            request.set_action_name('SendSms')
            
            # 设置请求参数
            request.add_query_param('RegionId', 'cn-hangzhou')
            request.add_query_param('PhoneNumbers', phone)
            request.add_query_param('SignName', settings.SMS_SIGN_NAME)
            request.add_query_param('TemplateCode', settings.SMS_TEMPLATE_CODE)
            
            # 模板参数（JSON格式）
            template_param = json.dumps({"code": code})
            request.add_query_param('TemplateParam', template_param)
            
            # 发送请求
            response = client.do_action_with_exception(request)
            response_data = json.loads(response.decode('utf-8'))
            
            # 检查响应
            if response_data.get('Code') == 'OK':
                logger.info(f"短信验证码发送成功: {phone}")
            else:
                logger.error(f"短信验证码发送失败: {response_data.get('Message')}")
                return None
                
        except ImportError:
            logger.warning("阿里云短信SDK未安装，使用开发模式")
            logger.info(f"[开发模式] 短信验证码 {phone}: {code}")
        except Exception as e:
            logger.error(f"发送短信失败: {str(e)}")
            # 开发环境即使失败也继续，生产环境应返回None
            if not settings.DEBUG:
                return None
            logger.info(f"[开发模式] 短信验证码 {phone}: {code}")
    else:
        # 开发环境：只记录日志，不真实发送
        logger.info(f"[开发模式] 短信验证码 {phone}: {code}")
    
    # 存储验证码（5分钟有效期）
    # 优先使用Redis缓存
    cache_key = f"sms_code:{phone}"
    await set_cache(cache_key, code, expire=300)
    
    # 同时存储在内存中（作为备用）
    sms_codes[phone] = {
        "code": code,
        "expires_at": asyncio.get_event_loop().time() + 300  # 5分钟
    }
    
    # 开发环境返回验证码，方便测试
    if settings.DEBUG:
        return code
    
    return None


async def verify_sms_code(phone: str, code: str) -> bool:
    """
    验证短信验证码
    
    Args:
        phone: 手机号
        code: 验证码
        
    Returns:
        是否验证成功
    """
    # 优先从Redis缓存获取
    cache_key = f"sms_code:{phone}"
    cached_code = await get_cache(cache_key)
    
    logger.debug(f"验证验证码: phone={phone}, code={code}, cached_code={cached_code}")
    
    if cached_code:
        # 确保比较的是字符串
        cached_code_str = str(cached_code).strip()
        code_str = str(code).strip()
        
        # 验证码正确
        if cached_code_str == code_str:
            # 验证成功后删除验证码（一次性使用）
            await delete_cache(cache_key)
            if phone in sms_codes:
                del sms_codes[phone]
            logger.info(f"验证码验证成功: {phone}")
            return True
        else:
            logger.warning(f"验证码不匹配: 期望={cached_code_str}, 实际={code_str}")
            return False
    
    # 从内存缓存获取（备用）
    if phone not in sms_codes:
        logger.warning(f"验证码不存在: {phone}")
        return False
    
    stored = sms_codes[phone]
    current_time = asyncio.get_event_loop().time()
    
    # 检查是否过期
    if current_time > stored["expires_at"]:
        del sms_codes[phone]
        logger.warning(f"验证码已过期: {phone}")
        return False
    
    # 验证码是否正确
    stored_code_str = str(stored["code"]).strip()
    code_str = str(code).strip()
    
    if stored_code_str != code_str:
        logger.warning(f"验证码不匹配: 期望={stored_code_str}, 实际={code_str}")
        return False
    
    # 验证成功后删除验证码（一次性使用）
    del sms_codes[phone]
    logger.info(f"验证码验证成功（内存缓存）: {phone}")
    return True


def cleanup_expired_codes():
    """清理过期的验证码"""
    current_time = asyncio.get_event_loop().time()
    expired_phones = [
        phone for phone, data in sms_codes.items()
        if current_time > data["expires_at"]
    ]
    for phone in expired_phones:
        del sms_codes[phone]

