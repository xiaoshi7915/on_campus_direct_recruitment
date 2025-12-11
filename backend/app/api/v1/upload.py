"""
文件上传相关API路由
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
from pathlib import Path

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.core.oss import oss_service
from app.schemas.upload import UploadResponse, UploadListResponse

router = APIRouter()

# 允许的文件类型
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp", "image/jpg"}
ALLOWED_DOCUMENT_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain"
}
ALLOWED_FILE_TYPES = ALLOWED_IMAGE_TYPES | ALLOWED_DOCUMENT_TYPES

# 文件大小限制（10MB）
MAX_FILE_SIZE = 10 * 1024 * 1024


def validate_file(file: UploadFile, max_size: int = MAX_FILE_SIZE) -> None:
    """
    验证文件
    
    Args:
        file: 上传的文件
        max_size: 最大文件大小（字节）
        
    Raises:
        HTTPException: 如果文件不符合要求
    """
    # 检查文件类型
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件类型：{file.content_type}。支持的类型：{', '.join(ALLOWED_FILE_TYPES)}"
        )
    
    # 注意：文件大小需要在读取时检查


@router.post("/image", response_model=UploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    file_type: str = Query("avatar", description="文件类型：avatar, resume, job, etc."),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    上传图片文件
    
    Args:
        file: 图片文件
        file_type: 文件类型
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        UploadResponse: 上传结果
        
    Raises:
        HTTPException: 如果文件不符合要求或上传失败
    """
    # 验证文件类型
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件类型：{file.content_type}。仅支持图片格式：{', '.join(ALLOWED_IMAGE_TYPES)}"
        )
    
    # 读取文件内容
    content = await file.read()
    
    # 检查文件大小
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"文件大小超过限制（最大{MAX_FILE_SIZE / 1024 / 1024}MB）"
        )
    
    try:
        # 生成文件路径
        file_path = oss_service.generate_file_path(file_type, file.filename)
        
        # 上传到OSS
        file_url = await oss_service.upload_file(
            content,
            file_path,
            content_type=file.content_type
        )
        
        return {
            "url": file_url,
            "file_path": file_path,
            "file_name": file.filename,
            "file_size": len(content),
            "content_type": file.content_type
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件上传失败：{str(e)}"
        )


@router.post("/document", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    file_type: str = Query("resume", description="文件类型：resume, job, etc."),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    上传文档文件（PDF、Word等）
    
    Args:
        file: 文档文件
        file_type: 文件类型
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        UploadResponse: 上传结果
        
    Raises:
        HTTPException: 如果文件不符合要求或上传失败
    """
    # 验证文件类型
    if file.content_type not in ALLOWED_DOCUMENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件类型：{file.content_type}。仅支持文档格式：{', '.join(ALLOWED_DOCUMENT_TYPES)}"
        )
    
    # 读取文件内容
    content = await file.read()
    
    # 检查文件大小
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"文件大小超过限制（最大{MAX_FILE_SIZE / 1024 / 1024}MB）"
        )
    
    try:
        # 生成文件路径
        file_path = oss_service.generate_file_path(file_type, file.filename)
        
        # 上传到OSS
        file_url = await oss_service.upload_file(
            content,
            file_path,
            content_type=file.content_type
        )
        
        return {
            "url": file_url,
            "file_path": file_path,
            "file_name": file.filename,
            "file_size": len(content),
            "content_type": file.content_type
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件上传失败：{str(e)}"
        )


@router.post("/batch", response_model=UploadListResponse)
async def upload_batch(
    files: List[UploadFile] = File(...),
    file_type: str = Query("general", description="文件类型"),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    批量上传文件
    
    Args:
        files: 文件列表
        file_type: 文件类型
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        UploadListResponse: 上传结果列表
        
    Raises:
        HTTPException: 如果文件不符合要求或上传失败
    """
    if len(files) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="一次最多上传10个文件"
        )
    
    uploaded_files = []
    
    for file in files:
        # 验证文件类型
        if file.content_type not in ALLOWED_FILE_TYPES:
            continue
        
        # 读取文件内容
        content = await file.read()
        
        # 检查文件大小
        if len(content) > MAX_FILE_SIZE:
            continue
        
        try:
            # 生成文件路径
            file_path = oss_service.generate_file_path(file_type, file.filename)
            
            # 上传到OSS
            file_url = await oss_service.upload_file(
                content,
                file_path,
                content_type=file.content_type
            )
            
            uploaded_files.append({
                "url": file_url,
                "file_path": file_path,
                "file_name": file.filename,
                "file_size": len(content),
                "content_type": file.content_type
            })
        except Exception as e:
            # 跳过失败的文件，继续处理其他文件
            continue
    
    return {
        "files": uploaded_files,
        "total": len(uploaded_files)
    }


@router.delete("/{file_path:path}")
async def delete_file(
    file_path: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    删除文件
    
    Args:
        file_path: 文件路径或URL
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        dict: 删除结果
        
    Raises:
        HTTPException: 如果删除失败
    """
    try:
        success = await oss_service.delete_file(file_path)
        if success:
            return {"message": "文件删除成功"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="文件删除失败"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件删除失败：{str(e)}"
        )

