# app/handlers/user_handlers.py

import logging

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from langchain_core.messages import AIMessage, HumanMessage

from app.config import settings
from app.core.chain import FallbackLoggingCallbackHandler, get_rag_chain
from app.core.memory import get_chat_memory
from app.utils.text_formatters import escape_markdown_v2, sanitize_for_telegram_markdown

# Create a new Router instance for user-facing handlers.
router = Router()


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