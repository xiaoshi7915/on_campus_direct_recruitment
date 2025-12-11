"""
文件上传相关Pydantic模式
"""
from pydantic import BaseModel, Field
from typing import Optional


class UploadResponse(BaseModel):
    """文件上传响应模式"""
    url: str = Field(..., description="文件URL")
    file_path: str = Field(..., description="文件路径")
    file_name: str = Field(..., description="文件名")
    file_size: int = Field(..., description="文件大小（字节）")
    content_type: Optional[str] = Field(None, description="文件MIME类型")


class UploadListResponse(BaseModel):
    """批量上传响应模式"""
    files: list[UploadResponse]
    total: int



