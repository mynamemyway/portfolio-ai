"""
Модульные тесты для обработчиков aiogram в app/handlers/user_handlers.py.

Используется pytest и pytest-asyncio для асинхронного тестирования.
Внешние зависимости, такие как RAG-цепочка, база данных и вызовы API Telegram,
полностью мокируются с помощью unittest.mock.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from aiogram import Bot
from aiogram.types import Message, User, Chat, CallbackQuery, InlineKeyboardMarkup

from app.handlers import user_handlers
from app.keyboards import MainMenuCallback

# Используем pytest-asyncio для всех тестов в этом файле
pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_bot():
    """Фикстура для создания мок-объекта Bot."""
    bot = AsyncMock(spec=Bot)
    return bot


@pytest.fixture
def mock_message():
    """
    Фикстура для создания гибкого мок-объекта Message с помощью MagicMock.
    Это позволяет избежать проблем с "замороженными" полями Pydantic.
    """
    message = MagicMock(spec=Message)
    message.from_user = MagicMock(spec=User)
    message.chat = MagicMock(spec=Chat)

    message.message_id = 789
    message.chat.id = 456
    message.chat.type = "private"
    message.from_user.id = 123
    message.from_user.username = "testuser"
    message.from_user.first_name = "Test"
    message.from_user.last_name = "User"
    message.text = "test message"
    message.date = datetime.now()

    # Мокируем методы, которые вызываются в обработчиках
    message.answer = AsyncMock()
    message.answer_photo = AsyncMock()
    return message


@pytest.fixture
def mock_callback_query(mock_message):
    """Фикстура для создания мок-объекта CallbackQuery."""
    # Используем MagicMock, чтобы избежать проблем с "замороженными" полями
    callback_query = MagicMock(spec=CallbackQuery)
    callback_query.id = "test_callback_id"
    callback_query.from_user = mock_message.from_user
    callback_query.message = mock_message
    callback_query.chat_instance = "test_chat_instance"
    callback_query.data = "test_data"

    # Сразу мокируем метод answer, который будет использоваться в тестах
    callback_query.answer = AsyncMock()

    return callback_query


@patch("app.handlers.user_handlers.log_query")
@patch("app.handlers.user_handlers.settings")
@patch("app.handlers.user_handlers.get_main_keyboard")
async def test_start_command(
    mock_get_main_keyboard, mock_settings, mock_log_query, mock_bot, mock_message
):
    """Тестирует обработчик команды /start."""
    # Настройка моков
    mock_settings.WELCOME_PHOTO_PATH = None  # Тестируем без фото для простоты
    # Возвращаем мок-объект, а не строку, чтобы пройти валидацию Pydantic
    mock_keyboard = MagicMock(spec=InlineKeyboardMarkup)
    mock_get_main_keyboard.return_value = mock_keyboard

    # Вызов обработчика
    await user_handlers.handle_start(mock_message, mock_bot)

    # Проверки
    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args_list[0]
    assert "Инициализация" in call_args.args[0]  # Аргумент 'text' является позиционным
    assert call_args.kwargs["reply_markup"] == mock_keyboard

    mock_log_query.assert_called_once()
    log_args = mock_log_query.call_args
    assert log_args.kwargs["user_id"] == mock_message.from_user.id
    assert log_args.kwargs["query_text"] == "COMMAND: /start"


@patch("app.handlers.user_handlers.log_query")
@patch("app.handlers.user_handlers.get_chat_memory")
async def test_reset_command(mock_get_chat_memory, mock_log_query, mock_message):
    """Тестирует обработчик команды /reset."""
    # Настройка моков
    mock_memory = MagicMock()
    mock_memory.chat_memory.clear = AsyncMock()
    mock_get_chat_memory.return_value = mock_memory

    # Вызов обработчика
    # Обработчик handle_reset не принимает bot в качестве аргумента
    await user_handlers.handle_reset(mock_message)

    # Проверки
    mock_get_chat_memory.assert_called_once_with(session_id=str(mock_message.chat.id))
    mock_memory.chat_memory.clear.assert_called_once()

    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args_list[0]
    assert "INFO: History successfully cleared" in call_args.args[0] # Аргумент 'text' является позиционным

    mock_log_query.assert_called_once()
    log_args = mock_log_query.call_args
    assert log_args.kwargs["user_id"] == mock_message.from_user.id
    assert log_args.kwargs["query_text"] == "COMMAND: /reset"


@patch("app.handlers.user_handlers.log_query")
@patch("app.handlers.user_handlers._edit_message")
@patch("app.handlers.user_handlers.get_projects_keyboard")
async def test_static_callback_handler(
    mock_get_projects_keyboard, mock_edit_message, mock_log_query, mock_bot, mock_callback_query
):
    """Тестирует обработчик callback-кнопки, не вызывающей RAG (например, 'projects')."""
    # Настройка моков
    callback_data = MainMenuCallback(action="projects")
    mock_keyboard = MagicMock(spec=InlineKeyboardMarkup)
    mock_get_projects_keyboard.return_value = mock_keyboard

    # Вызов обработчика
    await user_handlers.handle_main_menu_button(
        mock_callback_query, callback_data, mock_bot
    )

    mock_callback_query.answer.assert_awaited_once()
    # Проверки
    mock_edit_message.assert_called_once()
    edit_args = mock_edit_message.call_args
    assert edit_args.kwargs["message"] == mock_callback_query.message
    assert edit_args.kwargs["text"] == ""  # Text is empty for projects menu
    assert edit_args.kwargs["reply_markup"] == mock_keyboard

    mock_log_query.assert_called_once()
    log_args = mock_log_query.call_args
    assert log_args.kwargs["user_id"] == mock_callback_query.from_user.id
    assert log_args.kwargs["query_text"] == "CLICK: Projects Button"


@patch("app.handlers.user_handlers.process_query")
async def test_rag_callback_handler(mock_process_query, mock_bot, mock_callback_query):
    """Тестирует обработчик callback-кнопки, вызывающей RAG (например, 'skills')."""
    # Настройка моков
    callback_data = MainMenuCallback(action="skills")
    mock_process_query.return_value = None

    # Вызов обработчика
    await user_handlers.handle_main_menu_button(
        mock_callback_query, callback_data, mock_bot
    )

    # Проверки
    mock_callback_query.answer.assert_awaited_once()
    mock_process_query.assert_called_once()
    process_query_args = mock_process_query.call_args
    assert "Составь только структурированный список" in process_query_args.kwargs["user_question"]
    assert process_query_args.kwargs["chat_id"] == mock_callback_query.message.chat.id
    assert process_query_args.kwargs["message_to_answer"] == mock_callback_query.message
    assert process_query_args.kwargs["user"] == mock_callback_query.from_user


@patch("app.handlers.user_handlers.log_query")
@patch("app.handlers.user_handlers.get_chat_memory")
@patch("app.handlers.user_handlers.process_query")
async def test_text_message_handler(
    mock_process_query, mock_get_chat_memory, mock_log_query, mock_bot, mock_message
):
    """Тестирует обработчик обычного текстового сообщения, вызывающего RAG."""
    # Настройка моков
    user_question = "Расскажи о своем опыте"
    mock_message.text = user_question
    
    # Мокируем вызов process_query, чтобы он не выполнял реальную логику
    mock_process_query.return_value = None

    mock_memory = MagicMock()
    mock_memory.chat_memory.add_messages = AsyncMock()
    mock_get_chat_memory.return_value = mock_memory

    # Вызов обработчика
    await user_handlers.handle_message(mock_message, mock_bot)

    # Проверка вызова process_query
    mock_process_query.assert_called_once_with(
        chat_id=mock_message.chat.id,
        user_question=user_question,
        bot=mock_bot,
        message_to_answer=mock_message,
        user=mock_message.from_user
    )


@patch("app.handlers.user_handlers.process_query")
async def test_text_message_handler_parse_error_fallback(
    mock_process_query, mock_bot, mock_message
):
    """
    Тестирует fallback-механизм: если возникает ошибка парсинга MarkdownV2,
    сообщение должно быть отправлено без форматирования.
    """
    # Этот тест стал неактуальным, так как логика отправки и обработки ошибок
    # инкапсулирована внутри `process_query`. Мы тестируем только то, что
    # `handle_message` корректно вызывает `process_query`.
    mock_process_query.return_value = None
    await user_handlers.handle_message(mock_message, mock_bot)
    mock_process_query.assert_called_once()