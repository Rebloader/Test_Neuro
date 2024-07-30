import shutil

from typing import List
from fastapi import UploadFile
from concurrent.futures import ThreadPoolExecutor, Future, as_completed

from src.config import settings, BASE_DIR


def upload_file(file: UploadFile) -> str:
    """
    Синхронно загружаем файл с помощью shutil
    :param file: загружаемый на сервер файл
    :return: путь до загруженного файла
    """
    save_path: str = f'{BASE_DIR}/{settings.FILE_PATH}/{file.filename}'

    with open(save_path, 'wb') as f:
        shutil.copyfileobj(file.file, f)
    return save_path


def thread_upload_files(files: List[UploadFile]) -> List[str]:
    """
    Создаем пул потоков с ограничителем на кол-во задач, равное MAX_CHUNK_SIZE;
    через ThreadPoolExecutor отправляем их на выполнение и записываем в словарь с ключом по каждой Future
    проходим по коллекции выполненных Future и добавляем в список результатов
    :param files: список загружаемых на сервер файлов
    :return: список путей до загруженных файлов
    """

    results: List[str] = []

    with ThreadPoolExecutor(max_workers=settings.MAX_CHUNK_SIZE) as executor:
        futures: dict[Future, str] = {
            executor.submit(upload_file, file): file.filename for file in files
        }

        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    return results
