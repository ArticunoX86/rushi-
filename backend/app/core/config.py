from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Configuration
    Loads all environment variables from .env
    """

    # ==========================================================
    # Application
    # ==========================================================
    APP_NAME: str = "Real Estate AI Calling Platform"
    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # ==========================================================
    # Security
    # ==========================================================
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ==========================================================
    # Database
    # ==========================================================
    DATABASE_URL: str

    # ==========================================================
    # Gemini
    # ==========================================================
    GEMINI_API_KEY: str = ""

    # ==========================================================
    # OpenAI
    # ==========================================================
    OPENAI_API_KEY: str = ""

    # ==========================================================
    # Deepgram
    # ==========================================================
    DEEPGRAM_API_KEY: str = ""

    # ==========================================================
    # ElevenLabs
    # ==========================================================
    ELEVENLABS_API_KEY: str = ""
    ELEVENLABS_VOICE_ID: str = ""

    # ==========================================================
    # Cartesia
    # ==========================================================
    CARTESIA_API_KEY: str = ""
    CARTESIA_VOICE_ID: str = "a0e99841-438c-4a64-b6a9-ae8f1b115bbd"

    # ==========================================================
    # Salesforce
    # ==========================================================
    SALESFORCE_CLIENT_ID: str = ""
    SALESFORCE_CLIENT_SECRET: str = ""
    SALESFORCE_USERNAME: str = ""
    SALESFORCE_PASSWORD: str = ""
    SALESFORCE_SECURITY_TOKEN: str = ""
    SALESFORCE_LOGIN_URL: str = "https://login.salesforce.com"

    # ==========================================================
    # AWS
    # ==========================================================
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "ap-south-1"

    S3_BUCKET_NAME: str = ""
    CLOUDWATCH_LOG_GROUP: str = "real-estate-ai-calling"

    # ==========================================================
    # Android Gateway
    # ==========================================================
    ANDROID_GATEWAY_SECRET: str = ""
    ANDROID_GATEWAY_TIMEOUT: int = 30

    WEBSOCKET_HOST: str = "0.0.0.0"
    WEBSOCKET_PORT: int = 8765

    # ==========================================================
    # AI Configuration
    # ==========================================================
    AI_MODEL: str = "gemini-flash-latest"
    AI_TEMPERATURE: float = 0.15
    AI_MAX_TOKENS: int = 1000

    # ==========================================================
    # AI Safety Guardrails
    # ==========================================================
    AI_MAX_CALL_DURATION: int = 600           # 10 minutes max per call
    AI_MAX_TURNS_PER_CALL: int = 30           # Max conversation turns per call
    AI_MAX_RESPONSE_LENGTH: int = 500         # Max characters per AI response
    AI_ENABLE_INPUT_GUARDRAILS: bool = True    # Pre-processing input validation
    AI_ENABLE_OUTPUT_GUARDRAILS: bool = True   # Post-processing output validation
    AI_ENABLE_SENTIMENT_ALERTS: bool = True    # Sentiment-based supervisor alerts
    AI_ENABLE_STATE_MACHINE: bool = True       # Graph-based conversation flow

    # ==========================================================
    # Logging
    # ==========================================================
    LOG_LEVEL: str = "INFO"

    # ==========================================================
    # Pydantic Settings
    # ==========================================================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()