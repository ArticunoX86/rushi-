from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
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
from app.api.users import router as users_router
from app.api.roles import router as roles_router



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
    docs_url=None,
)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    html_content = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
    ).body.decode("utf-8")
    
    custom_css = """
    <style>
        body {
            background-color: #020617 !important;
            color: #f8fafc !important;
        }
        .swagger-ui .info .title, 
        .swagger-ui .info p, 
        .swagger-ui .info li, 
        .swagger-ui .info table, 
        .swagger-ui .info a,
        .swagger-ui .opblock .opblock-summary-operation-id, 
        .swagger-ui .opblock .opblock-summary-path, 
        .swagger-ui .opblock .opblock-summary-path__deprecated, 
        .swagger-ui .opblock .opblock-summary-description,
        .swagger-ui section.models h4,
        .swagger-ui .parameter__name,
        .swagger-ui .parameter__type,
        .swagger-ui .parameter__in,
        .swagger-ui .response-col_status, 
        .swagger-ui .response-col_description,
        .swagger-ui .model, .swagger-ui .model-title,
        .swagger-ui .tab li {
            color: #f8fafc !important;
        }
        .swagger-ui .opblock {
            background: rgba(30, 41, 59, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            backdrop-filter: blur(12px) !important;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1) !important;
        }
        .swagger-ui .opblock-body, .swagger-ui section.models .model-container {
            background: rgba(15, 23, 42, 0.6) !important;
            color: #f8fafc !important;
        }
        .swagger-ui section.models {
            background: rgba(30, 41, 59, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
        }
        .swagger-ui .btn.execute, .swagger-ui .btn.authorize {
            background-color: #3b82f6 !important;
            color: white !important;
            border-color: #3b82f6 !important;
            border-radius: 6px !important;
            box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2) !important;
        }
        .swagger-ui .btn.execute:hover, .swagger-ui .btn.authorize:hover {
            background-color: #2563eb !important;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.5) !important;
        }
        .swagger-ui .btn {
            border-color: rgba(255,255,255,0.2) !important;
            color: #f8fafc !important;
        }
        .swagger-ui .scheme-container {
            background-color: transparent !important;
            box-shadow: none !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        .swagger-ui table thead tr td, .swagger-ui table thead tr th {
            color: #94a3b8 !important;
            border-bottom-color: rgba(255,255,255,0.1) !important;
        }
        .swagger-ui .topbar {
            background-color: #0f172a !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        .swagger-ui .prop-type {
            color: #3b82f6 !important;
        }
        .swagger-ui input[type=text], .swagger-ui input[type=password], .swagger-ui input[type=search], .swagger-ui input[type=email], .swagger-ui input[type=file], .swagger-ui textarea, .swagger-ui select {
            background: rgba(15, 23, 42, 0.6) !important;
            color: #f8fafc !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            border-radius: 6px !important;
        }
        .swagger-ui .dialog-ux .modal-ux {
            background: #0f172a !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
        }
        .swagger-ui .dialog-ux .modal-ux-header h3 {
            color: #f8fafc !important;
        }
        .swagger-ui .dialog-ux .modal-ux-content h4 {
            color: #94a3b8 !important;
        }
    </style>
    """
    html_content = html_content.replace("</head>", f"{custom_css}</head>")
    return HTMLResponse(html_content)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

app.include_router(users_router)
app.include_router(roles_router)