import uvicorn
from fastapi import FastAPI

from src.routers.upload_router import router as upload_router


app = FastAPI()
app.include_router(upload_router)


if __name__ == '__main__':
    uvicorn.run(app)
