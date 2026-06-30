from fastapi import FastAPI

from app.core.config import settings
from app.core.logger import logger

logger.info("Backend Started Successfully")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Real Estate AI Calling Agent Backend"
)

@app.get("/")
async def root():
    logger.info("Root Endpoint Called")

    return {
        "status": "running",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/health")
async def health():
    logger.info("Health Check")

    return {
        "status": "healthy"
    }