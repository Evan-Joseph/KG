from datetime import datetime
from pydantic import BaseModel
from app.models.file import FileStatus


class FileBase(BaseModel):
    """文件基础模型"""
    filename: str
    file_type: str
    file_size: int


class FileCreate(FileBase):
    """文件创建模型"""
    original_filename: str


class FileUpdate(BaseModel):
    """文件更新模型"""
    status: FileStatus
    error_message: str | None = None


class FileInDB(FileBase):
    """数据库中的文件模型"""
    id: int
    original_filename: str
    status: FileStatus
    error_message: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FileResponse(FileInDB):
    """文件响应模型"""
    pass 