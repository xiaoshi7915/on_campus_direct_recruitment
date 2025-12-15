"""
中间件模块
包含日志、限流等中间件
"""
import time
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from collections import defaultdict
from app.core.logging import get_logger
from app.core.cache import get_redis

logger = get_logger(__name__)

# 内存限流器（Redis不可用时的降级方案）
rate_limiter = defaultdict(list)

class LoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # 记录请求信息
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # 记录响应信息
            logger.info(
                f"{request.method} {request.url.path} - "
                f"Status: {response.status_code} - "
                f"Time: {process_time:.3f}s"
            )
            
            # 添加处理时间到响应头
            response.headers["X-Process-Time"] = str(process_time)
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"{request.method} {request.url.path} - "
                f"Error: {str(e)} - "
                f"Time: {process_time:.3f}s",
                exc_info=True
            )
            raise


class RateLimitMiddleware(BaseHTTPMiddleware):
    """API限流中间件（使用Redis实现分布式限流）"""
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
    
    async def _check_rate_limit_redis(self, client_ip: str) -> bool:
        """
        使用Redis检查限流
        
        Returns:
            True: 允许请求
            False: 超过限制
        """
        redis = await get_redis()
        if not redis:
            return True  # Redis不可用时，降级到内存限流
        
        try:
            key = f"rate_limit:{client_ip}"
            current_count = await redis.incr(key)
            
            # 如果是第一次请求，设置过期时间
            if current_count == 1:
                await redis.expire(key, 60)  # 60秒过期
            
            # 检查是否超过限制
            if current_count > self.requests_per_minute:
                return False
            
            return True
        except Exception as e:
            logger.warning(f"Redis限流检查失败，降级到内存限流: {str(e)}")
            return None  # 返回None表示需要降级
    
    async def _check_rate_limit_memory(self, client_ip: str) -> bool:
        """
        使用内存检查限流（降级方案）
        
        Returns:
            True: 允许请求
            False: 超过限制
        """
        current_time = time.time()
        minute_ago = current_time - 60
        
        # 清理过期记录
        rate_limiter[client_ip] = [
            req_time for req_time in rate_limiter[client_ip]
            if req_time > minute_ago
        ]
        
        # 检查是否超过限制
        if len(rate_limiter[client_ip]) >= self.requests_per_minute:
            return False
        
        # 记录本次请求
        rate_limiter[client_ip].append(current_time)
        return True
    
    async def dispatch(self, request: Request, call_next):
        # 获取客户端IP
        client_ip = request.client.host if request.client else "unknown"
        
        # 跳过健康检查接口
        if request.url.path in ["/health", "/"]:
            return await call_next(request)
        
        # 先尝试使用Redis限流
        redis_result = await self._check_rate_limit_redis(client_ip)
        
        if redis_result is None:
            # Redis不可用，降级到内存限流
            if not await self._check_rate_limit_memory(client_ip):
                logger.warning(f"Rate limit exceeded for IP: {client_ip} (内存限流)")
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="请求过于频繁，请稍后再试"
                )
        elif not redis_result:
            # Redis限流：超过限制
            logger.warning(f"Rate limit exceeded for IP: {client_ip} (Redis限流)")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="请求过于频繁，请稍后再试"
            )
        
        return await call_next(request)


