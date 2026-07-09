from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.core.logger import logger

from app.database.session import engine


# ==================================================
# API ROUTERS IMPORT
# ==================================================

from app.api.auth import router as auth_router
from app.api.properties import router as property_router
from app.api.leads import router as lead_router
from app.api.calls import router as call_router
from app.api.conversations import router as conversation_router
from app.api.ai import router as ai_router
from app.api.speech import router as speech_router
from app.api.voice import router as voice_router
from app.api.voice_agent import router as voice_agent_router
from app.api.realtime_call import router as realtime_router



# ==================================================
# APPLICATION LIFESPAN
# ==================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    try:

        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )


        logger.info(
            "Database connected successfully."
        )


    except Exception as e:

        logger.error(
            f"Database connection failed: {e}"
        )


    yield



# ==================================================
# FASTAPI APP
# ==================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Real Estate AI Calling Platform Backend",
    lifespan=lifespan,
)



# ==================================================
# ROOT API
# ==================================================

@app.get("/")
async def root():

    return {
        "status": "running",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }



# ==================================================
# HEALTH CHECK
# ==================================================

@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }



# ==================================================
# REGISTER API ROUTERS
# ==================================================

app.include_router(
    auth_router
)


app.include_router(
    property_router
)


app.include_router(
    lead_router
)


app.include_router(
    call_router
)

app.include_router(
    conversation_router
)

app.include_router(
    ai_router
)

app.include_router(
    speech_router
)

app.include_router(
    voice_router
)

app.include_router(
    voice_agent_router
)

app.include_router(
    realtime_router
)