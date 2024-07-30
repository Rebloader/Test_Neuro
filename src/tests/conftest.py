import pytest
from fastapi import UploadFile
from io import BytesIO

pytest_plugins = ['pytest_asyncio']


@pytest.fixture
def files():
    return [
        UploadFile(filename="file1.txt", file=BytesIO(b"file1 content")),
        UploadFile(filename="file2.txt", file=BytesIO(b"file2 content")),
    ]
