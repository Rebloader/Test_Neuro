import pytest
import asyncio
from httpx import AsyncClient
from fastapi import UploadFile
from io import BytesIO

from src.main import app
from src.services.async_upload import async_upload_files


@pytest.mark.asyncio
async def test_async_upload_files(files):
    results = await async_upload_files(files)
    assert len(results) == 2
    assert "file1.txt" in results[0]
    assert "file2.txt" in results[1]


@pytest.mark.anyio
async def test_upload_files_async():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        files = [
            ('files', ('file1.txt', BytesIO(b'file1 content'), 'text/plain')),
            ('files', ('file2.txt', BytesIO(b'file2 content'), 'text/plain')),
        ]
        response = await ac.post("/upload/async", files=files)
    assert response.status_code == 201
    results = response.json().get('results')
    assert len(results) == 2
    assert 'file1.txt' in results[0]
    assert 'file2.txt' in results[1]



