import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy_utils import database_exists, create_database

from app.api_v1.router import api_router
from app.core.config import settings
from app.core.logger import init_logging
from app.db.database import Base, engine

app = FastAPI(
    title="vetis_parser",
    version="0.1.0",
    docs_url=f"{settings.API_V1_STR}/docs",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

init_logging()

if not database_exists(engine.url):
    create_database(engine.url)
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
