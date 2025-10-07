# app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    A class to manage application settings using Pydantic.
    It loads configuration from environment variables and/or a .env file.
    """
    # Telegram Bot Token from @BotFather
    BOT_TOKEN: str

    # Mistral AI API Key
    MISTRAL_API_KEY: str

    # Pydantic model configuration
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Create a single instance of the settings to be used throughout the application
settings = Settings()