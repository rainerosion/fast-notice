import uvicorn
from fastapi import FastAPI

from app.api.main import router

app = FastAPI()

app.include_router(router)
# app.include_router(item.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
