"""
OSS文件上传工具
"""
import oss2
from typing import Optional
import uuid
from datetime import datetime
from pathlib import Path
from app.core.config import settings


class OSSService:
    """
    OSS服务类，用于文件上传和管理
    """
    
    def __init__(self):
        """初始化OSS服务"""
        if not settings.OSS_ACCESS_KEY_ID or not settings.OSS_ACCESS_KEY_SECRET:
            self.auth = None
            self.bucket = None
            self.enabled = False
        else:
            # 创建OSS认证对象
            self.auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
            # 创建OSS服务端点
            endpoint = f"https://{settings.OSS_ENDPOINT}"
            # 创建Bucket对象
            self.bucket = oss2.Bucket(self.auth, endpoint, settings.OSS_BUCKET_NAME)
            self.enabled = True
    
    def generate_file_path(self, file_type: str, filename: str) -> str:
        """
        生成文件路径
        
        Args:
            file_type: 文件类型（avatar, resume, job, etc.）
            filename: 原始文件名
            
        Returns:
            str: 文件路径
        """
        # 获取文件扩展名
        ext = Path(filename).suffix
        # 生成唯一文件名
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        # 按日期组织目录结构
        date_str = datetime.now().strftime("%Y/%m/%d")
        # 生成完整路径
        file_path = f"{file_type}/{date_str}/{unique_filename}"
        return file_path
    
    async def upload_file(
        self,
        file_content: bytes,
        file_path: str,
        content_type: Optional[str] = None
    ) -> str:
        """
        上传文件到OSS
        
        Args:
            file_content: 文件内容（字节）
            file_path: 文件路径
            content_type: 文件MIME类型
            
        Returns:
            str: 文件URL
            
        Raises:
            Exception: 如果OSS未配置或上传失败
        """
        if not self.enabled:
            raise Exception("OSS未配置，无法上传文件")
        
        # 设置Content-Type
        headers = {}
        if content_type:
            headers['Content-Type'] = content_type
        
        # 上传文件
        result = self.bucket.put_object(file_path, file_content, headers=headers)
        
        if result.status == 200:
            # 生成文件URL
            file_url = f"https://{settings.OSS_BUCKET_NAME}.{settings.OSS_ENDPOINT}/{file_path}"
            return file_url
        else:
            raise Exception(f"文件上传失败，状态码：{result.status}")
    
    async def delete_file(self, file_path: str) -> bool:
        """
        删除OSS中的文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否删除成功
            
        Raises:
            Exception: 如果OSS未配置
        """
        if not self.enabled:
            raise Exception("OSS未配置，无法删除文件")
        
        try:
            # 从URL中提取路径
            if file_path.startswith("http"):
                # 提取路径部分
                file_path = file_path.split(f"{settings.OSS_BUCKET_NAME}.{settings.OSS_ENDPOINT}/")[-1]
            
            result = self.bucket.delete_object(file_path)
            return result.status == 204
        except Exception as e:
            print(f"删除文件失败：{e}")
            return False
    
    def get_file_url(self, file_path: str) -> str:
        """
        获取文件URL
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 文件URL
        """
        if file_path.startswith("http"):
            return file_path
        
        return f"https://{settings.OSS_BUCKET_NAME}.{settings.OSS_ENDPOINT}/{file_path}"


# 创建全局OSS服务实例
oss_service = OSSService()



