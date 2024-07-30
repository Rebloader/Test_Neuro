import logging
from functools import wraps
from fastapi import HTTPException

from src.config import settings


logger = logging.getLogger('upload_logger')
logger.setLevel(settings.LOG_LEVEL)

handler = logging.FileHandler(settings.LOG_FILE)
handler.setLevel(settings.LOG_LEVEL)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


def log_upload_operation(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get('files', [])
        try:
            result = await func(*args, **kwargs)
            logger.info(f'Successfully processed files: {[file.filename for file in request]}')
            return result
        except Exception as e:
            logger.error(f'Error processing files: {str(e)}')
            raise HTTPException(status_code=500, detail="An error occurred during file upload.")
    return wrapper
