# main.py

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from langchain_core.messages import AIMessage, HumanMessage

from app.config import settings
from app.core.chain import get_rag_chain
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


@router.message(CommandStart())
async def handle_start(message: Message):
    """
    Handles the /start command.
    Sends a welcome message to the user explaining the bot's purpose.
    """
    welcome_message = (
        "Инициализация...\n\n"
        "Протокол Portfolio AI v0.3.0 активирован.\n"
        "Я — цифровая копия Python-разработчика Александр.\n"  
        "Мои базы данных содержат полные стеки, архитектурные решения "
        "и детали реализации проекта PrimeNetworking.\n\n"  
        "Задайте вопрос, чтобы начать знакомство."
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
    try:
        ai_response = await rag_chain.ainvoke(
            {"session_id": session_id, "question": user_question}
        )

        # 4. Send the generated response back to the user
        await message.answer(ai_response)

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
        await message.answer("К сожалению, произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте еще раз позже.")


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
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    # Include the router in the dispatcher. This registers all handlers from the router.
    dp.include_router(router)

    # Start the polling process to receive updates from Telegram.
    # This will run indefinitely until the process is stopped.
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())