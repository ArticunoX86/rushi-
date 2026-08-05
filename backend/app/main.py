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
from app.api.devices import router as device_router
from app.api.device_socket import router as device_socket_router
from app.api.call_dispatch import router as call_dispatch_router
from app.api.logs import router as logs_router
from app.api.webrtc import router as webrtc_router
from app.api.dashboard import router as dashboard_router
from app.api.airtel_sip import router as airtel_sip_router
from app.api.analytics import router as analytics_router
from app.api.salesforce import router as salesforce_router
from app.api.endpoints.tata_webhooks import router as tata_webhook_router



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

app.include_router(
    device_router
)

app.include_router(
    device_socket_router
)

app.include_router(
    call_dispatch_router
)

app.include_router(
    logs_router
)

app.include_router(
    webrtc_router
)

app.include_router(
    dashboard_router
)

app.include_router(
    airtel_sip_router
)

app.include_router(
    analytics_router
)

app.include_router(
    salesforce_router
)

app.include_router(
    tata_webhook_router,
    prefix="/api/tata",
    tags=["TATA Telephony"]
)