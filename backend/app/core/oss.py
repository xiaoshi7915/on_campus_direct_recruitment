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
            # 创建OSS服务端点（如果endpoint已经包含https://，则不重复添加）
            if settings.OSS_ENDPOINT.startswith("https://"):
                endpoint = settings.OSS_ENDPOINT
            else:
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
            # 生成文件URL（如果endpoint已经包含https://，则使用bucket.endpoint格式）
            if settings.OSS_ENDPOINT.startswith("https://"):
                # endpoint格式：https://oss-cn-hangzhou.aliyuncs.com
                file_url = f"{settings.OSS_ENDPOINT}/{file_path}"
            else:
                # endpoint格式：oss-cn-hangzhou.aliyuncs.com
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
    
    def get_file_url(self, file_path: str, signed: bool = False, expires: int = 3600) -> str:
        """
        获取文件URL（支持生成签名URL）
        
        Args:
            file_path: 文件路径或完整URL
            signed: 是否生成签名URL（用于私有文件）
            expires: 签名URL有效期（秒），默认1小时
            
        Returns:
            str: 文件URL
        """
        if not self.enabled:
            return file_path
        
        # 如果输入是完整URL，提取路径部分（object_key）
        if file_path.startswith("http"):
            from urllib.parse import urlparse, unquote
            
            # 解析URL
            parsed = urlparse(file_path)
            
            # 提取object_key：从路径部分提取，去掉查询参数
            path = parsed.path.lstrip("/")
            
            # 如果路径以bucket名称开头，去掉它
            # 格式：https://bucket-name.oss-cn-hangzhou.aliyuncs.com/resume/2025/12/11/xxx.pdf
            # 或：https://bucket-name.oss-cn-hangzhou.aliyuncs.com/bucket-name/resume/2025/12/11/xxx.pdf
            if path.startswith(f"{settings.OSS_BUCKET_NAME}/"):
                path = path[len(f"{settings.OSS_BUCKET_NAME}/"):]
            
            # URL解码（可能被多次编码）
            object_key = path
            try:
                # 多次解码，直到无法再解码
                max_decode_iterations = 10
                for _ in range(max_decode_iterations):
                    new_decoded = unquote(object_key)
                    if new_decoded == object_key:
                        break
                    object_key = new_decoded
            except Exception as e:
                print(f"URL解码失败: {e}, 原始路径: {path}")
                # 解码失败，使用原始路径
            
            # 验证object_key是否有效（不能包含http、?、&等特殊字符）
            if not object_key or object_key.startswith("http") or "?" in object_key or "&" in object_key:
                # 如果提取失败，可能是格式不正确的URL
                print(f"无法从URL提取有效的object_key: {file_path}")
                # 如果已经是签名URL且不需要重新签名，直接返回
                if not signed and ("OSSAccessKeyId" in file_path or "Signature" in file_path):
                    return file_path
                # 否则返回原URL（虽然可能不正确）
                return file_path
            
            # 使用提取的object_key
            file_path = object_key
        
        if signed:
            # 生成签名URL（用于私有文件访问）
            try:
                # 确保file_path是有效的object_key（不包含特殊字符）
                if "?" in file_path or "&" in file_path or file_path.startswith("http"):
                    print(f"无效的object_key，无法生成签名URL: {file_path}")
                    # 如果已经是URL，尝试直接返回
                    if file_path.startswith("http"):
                        return file_path
                    # 否则生成公共URL
                    if settings.OSS_ENDPOINT.startswith("https://"):
                        return f"{settings.OSS_ENDPOINT}/{file_path}"
                    else:
                        return f"https://{settings.OSS_BUCKET_NAME}.{settings.OSS_ENDPOINT}/{file_path}"
                
                url = self.bucket.sign_url('GET', file_path, expires)
                return url
            except Exception as e:
                # 如果生成签名URL失败，返回原URL或生成公共URL
                print(f"生成签名URL失败: {e}, file_path: {file_path}")
                if file_path.startswith("http"):
                    return file_path
                if settings.OSS_ENDPOINT.startswith("https://"):
                    return f"{settings.OSS_ENDPOINT}/{file_path}"
                else:
                    return f"https://{settings.OSS_BUCKET_NAME}.{settings.OSS_ENDPOINT}/{file_path}"
        else:
            # 生成公共URL
            if settings.OSS_ENDPOINT.startswith("https://"):
                return f"{settings.OSS_ENDPOINT}/{file_path}"
            else:
                return f"https://{settings.OSS_BUCKET_NAME}.{settings.OSS_ENDPOINT}/{file_path}"


# 创建全局OSS服务实例
oss_service = OSSService()



