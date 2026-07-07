from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.core.logger import logger
from app.database.session import engine

from app.api.auth import router as auth_router
from app.api.properties import router as property_router

from app.api.leads import router as lead_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        logger.info("✅ Database connected successfully.")

    except Exception as e:

        logger.error(
            f"❌ Database connection failed: {e}"
        )


    yield



app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Real Estate AI Calling Platform Backend",
    lifespan=lifespan,
)



@app.get("/")
async def root():

    return {
        "status": "running",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }



@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }



# ==================================================
# API ROUTERS
# ==================================================

app.include_router(auth_router)

app.include_router(property_router)

app.include_router(lead_router)