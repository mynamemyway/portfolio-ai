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