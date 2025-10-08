# main.py

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import CommandStart, Message
from langchain_core.messages import AIMessage, HumanMessage

from app.config import settings
from app.core.chain import get_rag_chain
from app.core.memory import get_chat_memory

# Create a new Router instance. Routers are used to structure handlers.
router = Router()


@router.message(CommandStart())
async def handle_start(message: Message):
    """
    Handles the /start command.
    Sends a welcome message to the user explaining the bot's purpose.
    """
    welcome_message = (
        "Здравствуйте! Я — ваш персональный AI-ассистент по портфолио. "
        "Я здесь, чтобы ответить на ваши вопросы об опыте, проектах и "
        "технических навыках специалиста. Задайте мне вопрос."
    )
    await message.answer(welcome_message)


async def main() -> None:
    """
    Initializes and starts the Telegram bot.
    This function sets up the bot and dispatcher, registers handlers (in the future),
    and starts polling for updates from Telegram.
    """
    # Initialize Bot and Dispatcher instances. The bot token is read from the settings.
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    # Include the router in the dispatcher. This registers all handlers from the router.
    dp.include_router(router)

    # Start the polling process to receive updates from Telegram.
    # This will run indefinitely until the process is stopped.
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Configure logging to output to standard output with the INFO level.
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())