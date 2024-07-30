import pytest

from httpx import AsyncClient
from fastapi import UploadFile
from io import BytesIO

from src.main import app
from src.services.thread_upload import thread_upload_files


def test_thread_upload_files(files):
    results = thread_upload_files(files)
    assert len(results) == 2
    assert "file1.txt" in results[0]
    assert "file2.txt" in results[1]


@pytest.mark.asyncio
async def test_upload_files_thread():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        files = [
            ('files', ('file1.txt', BytesIO(b'file1 content'), 'text/plain')),
            ('files', ('file2.txt', BytesIO(b'file2 content'), 'text/plain')),
        ]
        response = await ac.post("/upload/thread", files=files)
    assert response.status_code == 201
    results = response.json().get('results')
    assert len(results) == 2
    assert 'file1.txt' in results[0]
    assert 'file2.txt' in results[1]
