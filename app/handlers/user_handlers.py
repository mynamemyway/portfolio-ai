# app/handlers/user_handlers.py

import logging
from pathlib import Path

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, FSInputFile, Message, InlineKeyboardMarkup, InputMediaPhoto, User
from langchain_core.messages import AIMessage, HumanMessage

from app.config import settings
from app.core.chain import FallbackLoggingCallbackHandler, get_rag_chain
from app.core.memory import get_chat_memory
from app.core.stats import log_query
from app.keyboards import (
    MainMenuCallback,
    get_contact_keyboard,
    get_main_keyboard,
    get_hello_world_keyboard,
    get_projects_keyboard,
    get_help_keyboard,
    get_skills_keyboard,
)
from app.utils.text_formatters import escape_markdown_v2, sanitize_for_telegram_markdown

# Create a new Router instance for user-facing handlers.
router = Router()

# Define the welcome message as a constant for reusability.
WELCOME_MESSAGE_TEXT = (
    "```python\n"
    "Инициализация...\n"
    "Протокол Portfolio AI ver 1.4.0 активирован.\n\n"
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
    "автоматизации бизнес процессов, проектировании асинхронных систем, "
    "LLM-интеграций и работе с данными.\n\n"
    "Я здесь, чтобы показать, какими навыками обладаю и как применил их в бизнес проектах."
    "```"
)

# Define the static text for the "/help" command.
HELP_MESSAGE_TEXT = (
    "```python\n"
    "#  Возможные Проблемы и Решения:\n"
    "1. Задержка Ответа: Из-за обращения к внешнему LLM API, ответ может занять 5-10 секунд. Пожалуйста, подождите.\n"
    "2. Бот Завис: Если бот не отвечает, попробуйте перезапустить командой: /start\n"
    "3. Неверный Контекст: Если AI сбился с темы, используйте команду /reset, чтобы очистить историю чата и начать диалог с чистого листа.\n\n"
    "#  Прямая Связь:\n"
    "Если у вас есть конкретные предложения по работе или вопросы, не предназначенные для AI-обсуждения, вы можете\n"
    "cвязаться со мной напрямую в telegram или по email:\n\n<samokhvaloff.on@gmail.com>\n"
    "```"
)

# Define the confirmation text for the /reset command.
RESET_CONFIRMATION_TEXT = (
    "```python\n"
    "INFO: History successfully cleared"
    "\n```"
)



@router.message(CommandStart())
async def handle_start(message: Message, bot: Bot):
    """Handles the /start command, sending a welcome message with a photo (if configured) and an inline keyboard for primary actions."""
    await log_query(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        query_text="COMMAND: /start",
    )
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
    await log_query(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        query_text="COMMAND: /help",
    )
    help_keyboard = get_help_keyboard()

    photo_path = settings.HELP_PHOTO_PATH
    # Check if a help photo path is configured and the file exists.
    if photo_path and Path(photo_path).is_file():
        photo = FSInputFile(photo_path)
        await message.answer_photo(
            photo=photo, caption=HELP_MESSAGE_TEXT, reply_markup=help_keyboard
        )
    else:
        # If the path is set but the file is not found, log a warning.
        if photo_path:
            logging.warning(
                f"Help photo file not found at the specified path: {photo_path}"
            )
        # Fallback to sending a text message if no photo is available.
        await message.answer(HELP_MESSAGE_TEXT, reply_markup=help_keyboard, parse_mode=None)


@router.message(Command("reset"))
async def handle_reset(message: Message):
    """
    Handles the /reset command by clearing the user's chat history.
    """
    await log_query(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        query_text="COMMAND: /reset",
    )
    session_id = str(message.chat.id)
    memory = get_chat_memory(session_id=session_id)
    await memory.chat_memory.clear()
    await message.answer(RESET_CONFIRMATION_TEXT)


async def process_query(
    chat_id: int, user_question: str, bot: Bot, message_to_answer: Message, user: User
):
    """A reusable function to process a user's query through the RAG chain.

    Args:
        chat_id: The user's chat ID for session management.
        user_question: The question to be processed.
        bot: The Bot instance to send 'typing' action.
        message_to_answer: The Message object to reply to or edit.
        user: The User object of the person who initiated the query.
    """
    # 1. Provide user feedback that the request is being processed
    await bot.send_chat_action(chat_id=chat_id, action="typing")

    # 3. Get the RAG chain and invoke it with the user's question
    rag_chain = get_rag_chain()
    # Create an instance of the callback handler to log fallbacks
    fallback_logger = FallbackLoggingCallbackHandler()
    try:
        result = await rag_chain.ainvoke(
            {"session_id": str(chat_id), "question": user_question},
            # Pass the callback handler to the chain invocation
            config={"callbacks": [fallback_logger]},
        )
        ai_response = result["answer"]
        retrieved_context = result["context"]

        # 4. Send the generated response based on the configuration setting
        if settings.RESPONSE_AS_CODE_BLOCK:
            # Sanitize the response to prevent breaking the code block and wrap it.
            safe_response = ai_response.replace("```", "`` ` ``")
            formatted_response = f"```\n{safe_response}\n```"
            # Send as a code block, which doesn't need Markdown parsing.
            await message_to_answer.answer(formatted_response, parse_mode=None)
        elif settings.SANITIZE_RESPONSE:
            # Proactively sanitize the response to make it compatible with MarkdownV2.
            sanitized_response = sanitize_for_telegram_markdown(ai_response)
            try:
                # Attempt to send the sanitized message.
                await message_to_answer.answer(sanitized_response)
            except TelegramBadRequest as e:
                # If the sanitized version fails, log the error and fall back to sending without parsing.
                logging.error(
                    f"Sanitized message failed to send. Error: {e}. Falling back to parse_mode=None."
                )
                logging.error(f"Original AI response: {ai_response}")
                logging.error(f"Sanitized response that failed: {sanitized_response}")
                # Send the original, unescaped response without any parsing.
                await message_to_answer.answer(ai_response, parse_mode=None)
        else:
            # If sanitization is disabled, try sending with default MarkdownV2,
            # then fall back to no parsing on error.
            try:
                await message_to_answer.answer(ai_response)
            except TelegramBadRequest as e:
                logging.warning(
                    f"MarkdownV2 parsing failed: {e}. Sending with parse_mode=None."
                )
                await message_to_answer.answer(ai_response, parse_mode=None)

        # 5. Log the query and response to the statistics database
        await log_query(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            query_text=user_question,
            retrieved_context=retrieved_context,
            llm_response=ai_response,
        )

        # 6. Manually save the context to the chat history
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
    message: Message,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
    photo_path: str | None = None,
):
    """
    A helper function to edit a message, handling text, caption, and media changes.

    Args:
        message: The message object to edit.
        text: The new text or caption for the message.
        reply_markup: The new inline keyboard markup.
        photo_path: The path to a new photo to replace the existing one.
    """
    # Case 1: A new photo is provided, and the message already has media.
    # We use edit_media to replace the photo, caption, and keyboard.
    if photo_path and Path(photo_path).is_file() and message.photo:
        photo = FSInputFile(photo_path)
        # Create a specific InputMediaPhoto object as required by the API.
        media = InputMediaPhoto(media=photo, caption=text)
        await message.edit_media(media=media, reply_markup=reply_markup)

    # Case 2: No new photo is provided, but the message has a caption.
    # We only edit the caption and keyboard.
    elif message.caption:
        await message.edit_caption(caption=text, reply_markup=reply_markup)

    # Case 3: The message is a simple text message.
    # We edit the text and keyboard.
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
            await log_query(
                user_id=query.from_user.id,
                username=query.from_user.username,
                first_name=query.from_user.first_name,
                last_name=query.from_user.last_name,
                query_text="CLICK: Hello Button",
            )
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
            await log_query(
                user_id=query.from_user.id,
                username=query.from_user.username,
                first_name=query.from_user.first_name,
                last_name=query.from_user.last_name,
                query_text="CLICK: Back to Portfolio AI Button",
            )
            try:
                # This handles the "back" button from the "Hello world!" view,
                # returning the user to the initial welcome message and main keyboard.
                await _edit_message(
                    query.message,
                    WELCOME_MESSAGE_TEXT,
                    reply_markup=get_main_keyboard(),
                    photo_path=settings.WELCOME_PHOTO_PATH,
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
        case "about_me":
            predefined_question = "Представься локанично как человек"
            await process_query(
                chat_id=query.message.chat.id,
                user_question=predefined_question,
                bot=bot,
                message_to_answer=query.message,
                user=query.from_user,
            )
        case "skills":
            await log_query(
                user_id=query.from_user.id,
                username=query.from_user.username,
                first_name=query.from_user.first_name,
                last_name=query.from_user.last_name,
                query_text="CLICK: Skills Button",
            )
            await _edit_message(query.message, "", reply_markup=get_skills_keyboard()
            )
        case "projects":
            await log_query(
                user_id=query.from_user.id,
                username=query.from_user.username,
                first_name=query.from_user.first_name,
                last_name=query.from_user.last_name,
                query_text="CLICK: Projects Button",
            )
            await _edit_message(
                query.message,
                "", reply_markup=get_projects_keyboard()
            )
        case "contact":
            await log_query(
                user_id=query.from_user.id,
                username=query.from_user.username,
                first_name=query.from_user.first_name,
                last_name=query.from_user.last_name,
                query_text="CLICK: Contact Button",
            )
            await _edit_message(
                query.message,
                "", reply_markup=get_contact_keyboard()
            )
        case "back_to_main":
            await log_query(
                user_id=query.from_user.id,
                username=query.from_user.username,
                first_name=query.from_user.first_name,
                last_name=query.from_user.last_name,
                query_text="CLICK: Back to Main Menu Button",
            )
            await _edit_message(
                query.message,
                WELCOME_MESSAGE_TEXT,
                reply_markup=get_main_keyboard(),
                photo_path=settings.WELCOME_PHOTO_PATH,
            )
        case "show_project_primenet":
            predefined_question = "Расскажи кратко о проекте PrimeNetworking."
            await process_query(
                chat_id=query.message.chat.id,
                user_question=predefined_question,
                bot=bot,
                message_to_answer=query.message,
                user=query.from_user,
            )
        case "show_project_portfolio_ai":
            predefined_question = "Расскажи кратко о работе Portfolio AI бота."
            await process_query(
                chat_id=query.message.chat.id,
                user_question=predefined_question,
                bot=bot,
                message_to_answer=query.message,
                user=query.from_user,
            )
        case "hard_skills":
            predefined_question = "Составь только структурированный список своих хардскилов, исключая конкретную информацию о проектах."
            await process_query(
                chat_id=query.message.chat.id,
                user_question=predefined_question,
                bot=bot,
                message_to_answer=query.message,
                user=query.from_user,
            )
        case "soft_skills":
            predefined_question = "Составь только структурированный список своих софтскилов, исключая конкретную информацию о проектах."
            await process_query(
                chat_id=query.message.chat.id,
                user_question=predefined_question,
                bot=bot,
                message_to_answer=query.message,
                user=query.from_user,
            )
        case "restart_session":
            await log_query(
                user_id=query.from_user.id,
                username=query.from_user.username,
                first_name=query.from_user.first_name,
                last_name=query.from_user.last_name,
                query_text="CLICK: Restart Session Button",
            )
            # Re-trigger the /start handler to send a fresh welcome message.
            await handle_start(query.message, bot)
        case "reset_chat":
            # Replicate the /reset logic for the callback button.
            await log_query(
                user_id=query.from_user.id,
                username=query.from_user.username,
                first_name=query.from_user.first_name,
                last_name=query.from_user.last_name,
                query_text="CLICK: Reset Chat Button",
            )
            session_id = str(query.message.chat.id)
            memory = get_chat_memory(session_id=session_id)
            await memory.chat_memory.clear()
            # Send a new message to confirm the action.
            await query.message.answer(RESET_CONFIRMATION_TEXT)
            # Edit the original /help message to remove the keyboard,
            # preventing users from clicking buttons again.


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
        user=message.from_user,
    )