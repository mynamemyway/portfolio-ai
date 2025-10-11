# main.py

import asyncio
import logging
import re
import sys

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from langchain_core.messages import AIMessage, HumanMessage

from app.config import settings
from app.core.chain import FallbackLoggingCallbackHandler, get_rag_chain
from app.core.memory import get_chat_memory

# Create a new Router instance. Routers are used to structure handlers.
router = Router()


class TelemetryFilter(logging.Filter):
    """
    A custom logging filter to suppress noisy telemetry errors from ChromaDB.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        # Suppress logs from ChromaDB's telemetry module
        return not record.name.startswith("chromadb.telemetry.product.posthog")


def escape_markdown_v2(text: str) -> str:
    """
    Escapes special characters for Telegram's MarkdownV2 parse mode.

    Args:
        text: The input string to be escaped.
    Returns:
        The string with all special MarkdownV2 characters escaped.
    """
    escape_chars = r"([_*\[\]()~`>#+\-=|{}.!])"
    return re.sub(escape_chars, r"\\\1", text)


def sanitize_for_telegram_markdown(text: str) -> str:
    """
    Proactively sanitizes text to make it compatible with Telegram's MarkdownV2.

    This function converts unsupported markdown (like headers) into a supported
    format and escapes specific characters that are known to cause parsing errors.

    Args:
        text: The raw string from the LLM to be sanitized.
    Returns:
        A sanitized string ready for Telegram's MarkdownV2 parser.
    """
    if not text:
        return ""

    processed_lines = []
    for line in text.split('\n'):
        # Preserve empty lines
        if not line.strip():
            processed_lines.append(line)
            continue

        # Make a copy to modify
        processed_line = line

        # Rule 1: Convert main headers (e.g., ### Title) to bold text.
        processed_line = re.sub(r'^\s*#+\s+(.+)', r'*\1*', processed_line)

        # Rule 2: Convert list headers (e.g., "- **Tools:**") to just bold text.
        processed_line = re.sub(r'^\s*-\s+(\*\*.*?\*\*)', r'\1', processed_line)

        # Rule 3: Convert indented list items (e.g., "  - Ruff") to use a bullet point.
        processed_line = re.sub(r'^(\s+)-\s+', r'\1• ', processed_line)

        # Rule 4: Convert any remaining top-level list items.
        processed_line = re.sub(r'^\s*-\s+', '• ', processed_line)

        # Rule 5: Convert standard markdown bold (**text**) to Telegram's MarkdownV2 bold (*text*).
        processed_line = re.sub(r'\*\*(.*?)\*\*', r'*\1*', processed_line)

        processed_lines.append(processed_line)

    # Join the lines back and perform a final escape of all special characters.
    sanitized_text = '\n'.join(processed_lines)

    # Final escape for all special characters not part of intended formatting.
    escape_chars = r"(?<!\\)([\[\]\(\)~`>+\-=|{}.!])"
    sanitized_text = re.sub(escape_chars, r'\\\1', sanitized_text)

    return sanitized_text


@router.message(CommandStart())
async def handle_start(message: Message):
    """
    Handles the /start command.
    Sends a welcome message to the user explaining the bot's purpose.
    """
    welcome_message = (
        "```python\n"
        "Инициализация...\n\n"
        "Протокол Portfolio AI v0.4.0 активирован.\n"
        "Я — цифровая копия Python разработчика Александра.\n"
        "Мои базы данных содержат полные стеки, архитектурные решения "
        "и детали реализации проекта PrimeNetworking.\n\n"
        "Задайте вопрос, чтобы начать знакомство.\n"
        "```"
    )
    await message.answer(welcome_message)


@router.message(F.text)
async def handle_message(message: Message, bot: Bot):
    """
    Handles incoming text messages.
    This is the core handler that processes user queries through the RAG chain.
    """
    # 1. Provide user feedback that the request is being processed
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # 2. Define a unique session ID for the user's chat history
    session_id = str(message.chat.id)
    user_question = message.text

    # 3. Get the RAG chain and invoke it with the user's question
    rag_chain = get_rag_chain()
    # Create an instance of the callback handler to log fallbacks
    fallback_logger = FallbackLoggingCallbackHandler()
    try:
        ai_response = await rag_chain.ainvoke(
            {"session_id": session_id, "question": user_question},
            # Pass the callback handler to the chain invocation
            config={"callbacks": [fallback_logger]},
        )

        # 4. Send the generated response based on the configuration setting
        if settings.RESPONSE_AS_CODE_BLOCK:
            # Sanitize the response to prevent breaking the code block and wrap it.
            safe_response = ai_response.replace("```", "`` ` ``")
            formatted_response = f"```\n{safe_response}\n```"
            await message.answer(formatted_response)
        else:
            # Proactively sanitize the response to make it compatible with MarkdownV2.
            sanitized_response = sanitize_for_telegram_markdown(ai_response)
            try:
                # Attempt to send the sanitized message.
                await message.answer(sanitized_response)
            except TelegramBadRequest as e:
                # If even the sanitized version fails, log the error and fall back to full escaping.
                logging.error(
                    f"Sanitized message failed to send. Error: {e}. Falling back to full escape."
                )
                logging.error(f"Original AI response: {ai_response}")
                logging.error(f"Sanitized response that failed: {sanitized_response}")
                escaped_response = escape_markdown_v2(ai_response)
                await message.answer(escaped_response)

        # 5. Manually save the context to the chat history
        # The RAG chain loads history, but saving is handled here.
        memory = get_chat_memory(session_id=session_id)
        await memory.chat_memory.add_messages(
            [HumanMessage(content=user_question), AIMessage(content=ai_response)]
        )
    except Exception as e:
        # Log the full error for debugging purposes
        logging.error(f"Error processing message for user {session_id}: {e}", exc_info=True)
        # Inform the user that an error occurred
        error_text = (
            "```python\n"
            "К сожалению, произошла ошибка при обработке вашего запроса.\n"
            "Пожалуйста, попробуйте еще раз позже.\n"
            "```"
        )
        await message.answer(error_text)


async def main() -> None:
    """
    Initializes and starts the Telegram bot.
    This function sets up the bot and dispatcher, registers handlers (in the future),
    and starts polling for updates from Telegram.
    """
    # Configure logging first to ensure handlers and filters are set up correctly.
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # Add the custom filter to the root logger to suppress ChromaDB telemetry errors
    telemetry_filter = TelemetryFilter()
    # Apply the filter to all existing handlers of the root logger.
    for handler in logging.getLogger().handlers:
        handler.addFilter(telemetry_filter)

    # Initialize Bot and Dispatcher instances. The bot token is read from the settings.
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="MarkdownV2"),
    )
    dp = Dispatcher()

    # Include the router in the dispatcher. This registers all handlers from the router.
    dp.include_router(router)

    # Start the polling process to receive updates from Telegram.
    # This will run indefinitely until the process is stopped.
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())