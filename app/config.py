# app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    A class to manage application settings using Pydantic.
    It loads configuration from environment variables and/or a .env file.
    """
    # Telegram Bot Token from @BotFather
    BOT_TOKEN: str

    # OpenRouter API Key
    OPENROUTER_API_KEY: str

    # URL for the self-hosted embedding service API
    EMBEDDING_SERVICE_URL: str
    
    # The specific chat model to use from OpenRouter
    # Best="google/gemini-2.0-flash-exp:free"
    OPENROUTER_CHAT_MODEL: str = "google/gemini-2.0-flash-exp:free"
    
    # The fallback model to use if the primary model fails
    OPENROUTER_FALLBACK_MODEL: str = "mistralai/mistral-medium-3.1"
    
    # The base URL for the OpenRouter API
    OPENROUTER_API_BASE: str = "https://openrouter.ai/api/v1"

    # Controls the creativity of the response (0.0 - 1.0)
    OPENROUTER_TEMPERATURE: float = 0.7

    # Limits the length of the generated response in tokens
    OPENROUTER_MAX_TOKENS: int = 1024
    
    # Number of messages to keep in the conversation window memory
    MEMORY_WINDOW_SIZE: int = 10

    # Pydantic model configuration
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Create a single instance of the settings to be used throughout the application
settings = Settings()