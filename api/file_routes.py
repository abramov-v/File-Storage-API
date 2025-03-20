import os
import shutil
import re
from datetime import datetime, timezone

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from api.auth_routes import get_current_user
from core.config import UPLOAD_FOLDER, MINIO_ENDPOINT, MINIO_BUCKET
from celery_app.celery_worker import process_file
from core.database import get_db
from core.minio_client import (
                        minio_client,
                        get_presigned_url,
                        delete_file_from_minio
                        )
from models.models import File as FileModel


router = APIRouter()


def sanitize_filename(filename: str) -> str:
    """Replacing special characters in filename."""
    return re.sub(r"[^\w.-]", "_", filename)


@router.post('/upload')
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    """Upload file to local storage and MinIO."""
    file_key = sanitize_filename(file.filename)
    file_size = file.size
    file_path = os.path.join(UPLOAD_FOLDER, file_key)

    print(f"[DEBUG] Saving file as: {file_key} -> {file_path}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(file_path, "rb") as f:
        minio_client.upload_fileobj(f, MINIO_BUCKET, file_key)

    file_url = f'{MINIO_ENDPOINT}/{MINIO_BUCKET}/{file_key}'

    uploaded_at = datetime.now(timezone.utc)

    new_file = FileModel(
        filename=file_key,
        file_url=file_url,
        size=file_size,
        uploaded_at=uploaded_at
    )
    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)

    return {'filename': file.filename,
            'file_url': file_url,
            'file_size': file_size}


@router.get('/files/')
async def get_files(filename: str = Query(None, description='Filter filename'),
                    db: AsyncSession = Depends(get_db)
                    ):
    """Retrieve list of files, optionally filtered by filename."""
    query = select(FileModel)

    if filename:
        query = query.where(func.lower(FileModel.filename).
                            contains(filename.lower()))

    result = await db.execute(query)
    files = result.scalars().all()

    return [
        {
            "id": file.id,
            "filename": file.filename,
            "file_url": file.file_url,
            "size": file.size,
            "uploaded_at": file.uploaded_at
        }
        for file in files
    ]


@router.delete('/files/{file_key}')
async def delete_file(file_key: str,
                      db: AsyncSession = Depends(get_db),
                      user: str = Depends(get_current_user)
                      ):
    """Delete file from the database and MinIO."""
    result = await db.execute(select(FileModel).
                              where(FileModel.filename == file_key))
    file_record = result.scalars().first()

    if not file_record:
        raise HTTPException(status_code=404,
                            detail="File not found in database")

    if not delete_file_from_minio(file_key):
        raise HTTPException(status_code=500,
                            detail="Error deleting file from MinIO")

    await db.delete(file_record)
    await db.commit()

    return {"message": "File successfully deleted", "filename": file_key}


@router.post('/process/{file_name}')
async def start_processing(file_name: str):
    """Send file for processing in Celery."""
    sanitized_file_name = sanitize_filename(file_name)

    print(f"[DEBUG] Sending file '{sanitized_file_name}' for processing...")
    task = process_file.delay(sanitized_file_name)

    return {"message": "File sent for processing",
            "task_id": task.id,
            "sanitized_name": sanitized_file_name}


@router.get('/download/{file_key}')
async def generate_download_link(file_key: str):
    """Generate a download link for file."""
    url = get_presigned_url(file_key)

    if not url:
        raise HTTPException(status_code=404, detail='File not found')

    return {'download_url': url}
