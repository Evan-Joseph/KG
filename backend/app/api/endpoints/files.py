import os
from typing import List
from fastapi import APIRouter, Depends, UploadFile, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.models.file import File, FileStatus
from app.schemas.file import FileResponse, FileCreate
from app.services.file_processor import process_file

settings = get_settings()
router = APIRouter()


def validate_file(file: UploadFile):
    """验证上传的文件"""
    # 检查文件大小
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    
    if size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"文件大小超过限制：{settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
        )
    
    # 检查文件类型
    ext = file.filename.split('.')[-1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型：{ext}"
        )


@router.post("/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """上传文件接口"""
    validate_file(file)
    
    # 确保上传目录存在
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # 生成唯一文件名
    ext = file.filename.split('.')[-1].lower()
    filename = f"{os.urandom(16).hex()}.{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    
    # 保存文件
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败：{str(e)}")
    
    # 创建文件记录
    file_create = FileCreate(
        filename=filename,
        original_filename=file.filename,
        file_type=ext,
        file_size=len(contents)
    )
    db_file = File(**file_create.model_dump())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    # 添加后台处理任务
    background_tasks.add_task(process_file, file_path, db_file.id)
    
    return db_file


@router.get("/files", response_model=List[FileResponse])
def list_files(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """获取文件列表"""
    files = db.query(File).offset(skip).limit(limit).all()
    return files


@router.get("/files/{file_id}", response_model=FileResponse)
def get_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    """获取文件详情"""
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="文件不存在")
    return file 