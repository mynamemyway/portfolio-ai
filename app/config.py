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

    # Number of messages to keep in the conversation window memory
    MEMORY_WINDOW_SIZE: int = 10

    # The specific chat model to use from Mistral AI
    MISTRAL_CHAT_MODEL: str = "mistral-small-latest"

    # Disable anonymous telemetry for ChromaDB to prevent errors and unnecessary network requests.
    # See: https://docs.trychroma.com/telemetry
    # The value should be a string 'False' as ChromaDB checks for the string representation.
    ANONYMIZED_TELEMETRY: str = "False"

    # Pydantic model configuration
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Create a single instance of the settings to be used throughout the application
settings = Settings()