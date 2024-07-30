import aiofiles
import asyncio

from typing import List
from fastapi import UploadFile

from src.config import settings, BASE_DIR


async def upload_file(file: UploadFile) -> str:
    """
    Асинхронно загружает файл с помощью aiofiles
    :param file: загружаемый на сервер файл
    :return: путь до загруженного файла
    """
    save_path: str = f'{BASE_DIR}/{settings.FILE_PATH}/{file.filename}'
    async with aiofiles.open(save_path, 'wb') as f:
        await f.write(await file.read())
    return save_path


async def async_upload_files(files: List[UploadFile]) -> List[str]:
    """
    Создает ограничитель limiter для максимального количества обработки файлов за момент времени;
    создает задачи для всех загружаемых файлов и ожидает завершения их выполнения
    :param files: список загружаемых на сервер файлов
    :return: список путей до загруженных файлов
    """
    limiter = asyncio.Semaphore(settings.MAX_CHUNK_SIZE)

    async def upload_with_semaphore(file: UploadFile):
        async with limiter:
            return await upload_file(file=file)  # Асинхронная загрузка файла

    tasks: list = [upload_with_semaphore(file) for file in files]  # Создание задач для всех файлов
    results = await asyncio.gather(*tasks)  # Ожидание выполнения всех задач
    return results
