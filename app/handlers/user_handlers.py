# app/handlers/user_handlers.py

import logging
from pathlib import Path

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, FSInputFile, Message, InlineKeyboardMarkup
from langchain_core.messages import AIMessage, HumanMessage

from app.config import settings
from app.core.chain import FallbackLoggingCallbackHandler, get_rag_chain
from app.core.memory import get_chat_memory
from app.keyboards import (
    MainMenuCallback,
    get_contact_keyboard,
    get_main_keyboard,
    get_hello_world_keyboard,
    get_projects_keyboard,
    get_help_keyboard,
)
from app.utils.text_formatters import escape_markdown_v2, sanitize_for_telegram_markdown

# Create a new Router instance for user-facing handlers.
router = Router()

# Define the welcome message as a constant for reusability.
WELCOME_MESSAGE_TEXT = (
    "```python\n"
    "Инициализация...\n"
    "Протокол Portfolio AI v1.0.0 активирован.\n\n"
    "Я — ваш персональный AI-интерфейс к опыту Python-разработчика Александра. "
    "Мои базы данных содержат полные стеки, архитектурные решения и детали реализации проектов.\n\n"
    "Начните с команды 'Hello world!' или задайте свой вопрос,чтобы начать извлечение данных."
    "```"
)

# Define the static text for the "Hello world!" button.
HELLO_WORLD_TEXT = (
    "```python\n"
    "`Hello world!`\n"
    "Рад приветствовать вас в моём AI-портфолио.\n\n"
    "Меня зовут Александр, я — Python Backend Developer. Специализируюсь на "
    "проектировании и реализации асинхронных, масштабируемых систем и LLM-интеграций.\n\n"
    "Я здесь, чтобы показать, какими навыками обладаю и как применил их в бизнес проектах."
    "```"
)

# Define the static text for the "/help" command.
HELP_MESSAGE_TEXT = (
    "```python\n"
    "## Возможные Проблемы и Решения:\n"
    "1.  **Задержка Ответа:** Из-за обращения к внешнему LLM API, ответ может занять 5-10 секунд. Пожалуйста, подождите.\n"
    "2.  **Бот Завис/Остановился:** Если бот не отвечает, попробуйте перезапустить сессию командой: /start\n"
    "3.  **Неверный Контекст:** Если AI сбился с темы, используйте команду /reset, чтобы очистить историю чата и начать диалог с чистого листа.\n\n"
    "## Прямая Связь:\n"
    "Если у вас есть конкретные предложения по работе или вопросы, не предназначенные для AI-обсуждения, вы всегда можете:\n"
    "📞 **Связаться со мной напрямую:** https://t.me/mynamemyway , samokhvaloff.on@gmail.com\n"
    "```"
)

# Define the confirmation text for the /reset command.
RESET_CONFIRMATION_TEXT = (
    "```python\n"
    "INFO: История вашего диалога успешно очищена."
    "\n```"
)



@router.message(CommandStart())
async def handle_start(message: Message, bot: Bot):
    """Handles the /start command, sending a welcome message with a photo (if configured) and an inline keyboard for primary actions."""
    main_keyboard = get_main_keyboard()

    photo_path = settings.WELCOME_PHOTO_PATH
    # Check if a welcome photo path is configured and the file exists.
    if photo_path and Path(photo_path).is_file():
        photo = FSInputFile(photo_path)
        await message.answer_photo(
            photo=photo, caption=WELCOME_MESSAGE_TEXT, reply_markup=main_keyboard
        )
    else:
        # If the path is set but the file is not found, log a warning.
        if photo_path:
            logging.warning(
                f"Welcome photo file not found at the specified path: {photo_path}"
            )
        # Fallback to sending a text message if no photo is available.
        await message.answer(WELCOME_MESSAGE_TEXT, reply_markup=main_keyboard)


@router.message(Command("help"))
async def handle_help(message: Message):
    """Handles the /help command by sending a static informational message."""
    await message.answer(HELP_MESSAGE_TEXT, reply_markup=get_help_keyboard())


@router.message(Command("reset"))
async def handle_reset(message: Message):
    """
    Handles the /reset command by clearing the user's chat history.
    """
    session_id = str(message.chat.id)
    memory = get_chat_memory(session_id=session_id)
    await memory.chat_memory.clear()
    await message.answer(RESET_CONFIRMATION_TEXT)


async def process_query(
    chat_id: int, user_question: str, bot: Bot, message_to_answer: Message
):
    """A reusable function to process a user's query through the RAG chain.

    Args:
        chat_id: The user's chat ID for session management.
        user_question: The question to be processed.
        bot: The Bot instance to send 'typing' action.
        message_to_answer: The Message object to reply to.
    """
    # 1. Provide user feedback that the request is being processed
    await bot.send_chat_action(chat_id=chat_id, action="typing")

    # 3. Get the RAG chain and invoke it with the user's question
    rag_chain = get_rag_chain()
    # Create an instance of the callback handler to log fallbacks
    fallback_logger = FallbackLoggingCallbackHandler()
    try:
        ai_response = await rag_chain.ainvoke(
            {"session_id": str(chat_id), "question": user_question},
            # Pass the callback handler to the chain invocation
            config={"callbacks": [fallback_logger]},
        )

        # 4. Send the generated response based on the configuration setting
        if settings.RESPONSE_AS_CODE_BLOCK:
            # Sanitize the response to prevent breaking the code block and wrap it.
            safe_response = ai_response.replace("```", "`` ` ``")
            formatted_response = f"```\n{safe_response}\n```"
            await message_to_answer.answer(formatted_response)
        else:
            # Proactively sanitize the response to make it compatible with MarkdownV2.
            sanitized_response = sanitize_for_telegram_markdown(ai_response)
            try:
                # Attempt to send the sanitized message.
                await message_to_answer.answer(sanitized_response)
            except TelegramBadRequest as e:
                # If even the sanitized version fails, log the error and fall back to full escaping.
                logging.error(
                    f"Sanitized message failed to send. Error: {e}. Falling back to full escape."
                )
                logging.error(f"Original AI response: {ai_response}")
                logging.error(f"Sanitized response that failed: {sanitized_response}")
                escaped_response = escape_markdown_v2(ai_response)
                await message_to_answer.answer(escaped_response)

        # 5. Manually save the context to the chat history
        # The RAG chain loads history, but saving is handled here.
        memory = get_chat_memory(session_id=str(chat_id))
        await memory.chat_memory.add_messages(
            [HumanMessage(content=user_question), AIMessage(content=ai_response)]
        )
    except Exception as e:
        # Log the full error for debugging purposes
        logging.error(f"Error processing message for user {chat_id}: {e}", exc_info=True)
        # Inform the user that an error occurred
        error_text = (
            "```python\n"
            "К сожалению, произошла ошибка при обработке вашего запроса.\n"
            "Пожалуйста, попробуйте еще раз позже.\n"
            "```"
        )
        await message_to_answer.answer(error_text)


async def _edit_message(
    message: Message, text: str, reply_markup: InlineKeyboardMarkup | None = None
):
    """
    A helper function to edit a message, handling both text and caption cases.

    This function checks if the message has a caption (i.e., it's a photo message)
    or regular text and uses the appropriate edit method to avoid Telegram API errors.

    Args:
        message: The message object to edit.
        text: The new text or caption for the message.
        reply_markup: The new inline keyboard markup.
    """
    if message.caption:
        await message.edit_caption(caption=text, reply_markup=reply_markup)
    else:
        await message.edit_text(text=text, reply_markup=reply_markup)


@router.callback_query(MainMenuCallback.filter())
async def handle_main_menu_button(
    query: CallbackQuery, callback_data: MainMenuCallback, bot: Bot
):
    """Handles presses of the main menu's inline keyboard buttons."""
    # Acknowledge the callback to remove the "loading" state from the button.
    await query.answer()

    # Ensure there's a message to edit.
    if not query.message:
        return

    match callback_data.action:
        case "hello":
            try:
                # Edit the message to show the static "Hello world!" text and
                # switch to the alternative keyboard with a "back" button.
                await _edit_message(
                    query.message,
                    HELLO_WORLD_TEXT, reply_markup=get_hello_world_keyboard()
                )
            except TelegramBadRequest as e:
                # This error occurs if the user repeatedly clicks the button.
                # The API returns an error because the message content is not modified.
                # We catch and ignore this specific error to avoid polluting the logs.
                if "message is not modified" in str(e):
                    pass
                else:
                    # Re-raise any other TelegramBadRequest errors for debugging.
                    raise
        case "about_portfolio":
            try:
                # This handles the "back" button from the "Hello world!" view,
                # returning the user to the initial welcome message and main keyboard.
                await _edit_message(
                    query.message, WELCOME_MESSAGE_TEXT, reply_markup=get_main_keyboard()
                )
            except TelegramBadRequest as e:
                # This error occurs if the user repeatedly clicks the button.
                # The API returns an error because the message content is not modified.
                # We catch and ignore this specific error to avoid polluting the logs.
                if "message is not modified" in str(e):
                    pass
                else:
                    # Re-raise any other TelegramBadRequest errors for debugging.
                    raise
        case "skills":
            predefined_question = "Расскажи кратко о своих профессиональных навыках и технологическом стеке."
            await process_query(
                chat_id=query.message.chat.id,
                user_question=predefined_question,
                bot=bot,
                message_to_answer=query.message,
            )
        case "projects":
            await _edit_message(
                query.message,
                "Select action:", reply_markup=get_projects_keyboard()
            )
        case "contact":
            await _edit_message(
                query.message,
                "Select method:", reply_markup=get_contact_keyboard()
            )
        case "back_to_main":
            await _edit_message(
                query.message,
                WELCOME_MESSAGE_TEXT, reply_markup=get_main_keyboard()
            )
        case "show_project_primenet":
            predefined_question = "Расскажи кратко о проекте PrimeNet."
            await process_query(
                chat_id=query.message.chat.id,
                user_question=predefined_question,
                bot=bot,
                message_to_answer=query.message,
            )
        case "restart_session":
            # Re-trigger the /start handler to send a fresh welcome message.
            await handle_start(query.message, bot)
        case "reset_chat":
            # Replicate the /reset logic for the callback button.
            session_id = str(query.message.chat.id)
            memory = get_chat_memory(session_id=session_id)
            await memory.chat_memory.clear()
            # Send a new message to confirm the action.
            await query.message.answer(RESET_CONFIRMATION_TEXT)
            # Edit the original /help message to remove the keyboard,
            # preventing users from clicking buttons again.
            await query.message.edit_reply_markup(reply_markup=None)


@router.message(F.text)
async def handle_message(message: Message, bot: Bot):
    """Handles incoming text messages by passing them to the query processor."""
    if not message.text:
        return
    if not message.text:
        return

    await process_query(
        chat_id=message.chat.id,
        user_question=message.text,
        bot=bot,
        message_to_answer=message,
    )