import asyncio
from typing import List

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from src.services.async_upload import async_upload_files
from src.services.thread_upload import thread_upload_files

router = APIRouter(prefix='/upload')


@router.post('/async')
async def upload_files_async(files: List[UploadFile] = File(...)) -> JSONResponse:
    """
    Асинхронная загрузка файлов на сервер
    """
    results = await async_upload_files(files=files)

    return JSONResponse(content={"results": results}, status_code=201)


@router.post('/thread')
def upload_files_thread(files: List[UploadFile] = File(...)) -> JSONResponse:
    """
    Загрузка файлов при помощи threading
    """
    results = thread_upload_files(files=files)

    return JSONResponse(content={"results": results}, status_code=201)
