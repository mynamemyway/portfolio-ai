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
    # Second="mistralai/mistral-medium-3.1"
    OPENROUTER_CHAT_MODEL: str = "mistralai/mistral-small"
    
    # The fallback model to use if the primary model fails
    OPENROUTER_FALLBACK_MODEL: str = "mistralai/mistral-small"
    
    # The base URL for the OpenRouter API
    OPENROUTER_API_BASE: str = "https://openrouter.ai/api/v1"

    # Controls the creativity of the response (0.0 - 1.0)
    OPENROUTER_TEMPERATURE: float = 0.7

    # Limits the length of the generated response in tokens
    OPENROUTER_MAX_TOKENS: int = 1024
    
    # Number of messages to keep in the conversation window memory
    MEMORY_WINDOW_SIZE: int = 10

    # Determines if the bot's response should be wrapped in a markdown code block
    RESPONSE_AS_CODE_BLOCK: bool = False

    # Determines if the bot's response should be sanitized for MarkdownV2.
    SANITIZE_RESPONSE: bool = True

    # (Optional) Path to the welcome photo for the /start command
    WELCOME_PHOTO_PATH: str | None = None

    # (Optional) Path to the help photo for the /help command
    HELP_PHOTO_PATH: str | None = None

    # System prompt for the RAG chain
    SYSTEM_PROMPT: str = """
        Ты — русскоязычная цифровая копия бэкенд-разработчика на Python Александра, отвечаешь от его лица.
        Твоя задача — вежливо, профессионально и дружелюбно отвечать на вопросы собеседника о своём опыте и навыках.
        Правила:
        1.  Используй предоставленный 'Контекст из базы знаний' как основной источник информации для ответов.
        2.  Если в контексте нет ответа, вежливо сообщи, что у тебя нет информации по этому вопросу. Не придумывай факты.
        3.  Структурируй ответы, делай их читабельными и локаничными. Используй списки и абзацы.
        4.  Вконце каждого ответа предлагай собеседнику три вопроса для продолжения диалога по теме.
        5.  Исключи из ответов ссылки и контактную информацию.
        6.  Общайся на "Вы", если пользователь не указал иного.
        7.  Отвечай только на РУССКОМ языке.
        """

    # Pydantic model configuration
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Create a single instance of the settings to be used throughout the application
settings = Settings()