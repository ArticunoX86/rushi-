from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ==========================
    # Application
    # ==========================
    APP_NAME: str = "Salesforce AI Calling Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # ==========================
    # Database
    # ==========================
    DATABASE_URL: str = ""

    # ==========================
    # OpenAI
    # ==========================
    OPENAI_API_KEY: str = ""

    # ==========================
    # Deepgram
    # ==========================
    DEEPGRAM_API_KEY: str = ""

    # ==========================
    # ElevenLabs
    # ==========================
    ELEVENLABS_API_KEY: str = ""

    # ==========================
    # AWS
    # ==========================
    AWS_ACCESS_KEY: str = ""
    AWS_SECRET_KEY: str = ""
    AWS_REGION: str = "ap-south-1"

    # ==========================
    # Salesforce
    # ==========================
    SALESFORCE_CLIENT_ID: str = ""
    SALESFORCE_CLIENT_SECRET: str = ""
    SALESFORCE_USERNAME: str = ""
    SALESFORCE_PASSWORD: str = ""
    SALESFORCE_SECURITY_TOKEN: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()