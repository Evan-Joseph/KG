from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
import enum

from app.db.session import Base


class FileStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class File(Base):
    """文件模型"""
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)  # 以字节为单位
    status = Column(SQLEnum(FileStatus), default=FileStatus.PENDING)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 