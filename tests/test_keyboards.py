# tests/test_keyboards.py

from aiogram.types import InlineKeyboardMarkup

from app.keyboards import (
    MainMenuCallback,
    get_contact_keyboard,
    get_hello_world_keyboard,
    get_help_keyboard,
    get_main_keyboard,
    get_projects_keyboard,
)


def test_get_main_keyboard():
    """Tests the get_main_keyboard function."""
    keyboard = get_main_keyboard()
    assert isinstance(keyboard, InlineKeyboardMarkup)

    buttons = {btn.text: btn for row in keyboard.inline_keyboard for btn in row}

    assert "➡️ Hello world!" in buttons
    assert buttons["➡️ Hello world!"].callback_data == MainMenuCallback(
        action="hello"
    ).pack()
    assert "Skills" in buttons
    assert buttons["Skills"].callback_data == MainMenuCallback(action="skills").pack()


def test_get_hello_world_keyboard():
    """Tests the get_hello_world_keyboard function."""
    keyboard = get_hello_world_keyboard()
    assert isinstance(keyboard, InlineKeyboardMarkup)

    buttons = {btn.text: btn for row in keyboard.inline_keyboard for btn in row}

    assert "⬅️ about Portfolio AI" in buttons
    assert buttons["⬅️ about Portfolio AI"].callback_data == MainMenuCallback(
        action="about_portfolio"
    ).pack()


def test_get_projects_keyboard():
    """Tests the get_projects_keyboard function."""
    keyboard = get_projects_keyboard()
    assert isinstance(keyboard, InlineKeyboardMarkup)

    buttons = {btn.text: btn for row in keyboard.inline_keyboard for btn in row}

    assert "Tell about PrimeNetworking" in buttons
    assert buttons["Tell about PrimeNetworking"].callback_data == MainMenuCallback(
        action="show_project_primenet"
    ).pack()
    assert "⬅️ Return" in buttons
    assert buttons["⬅️ Return"].callback_data == MainMenuCallback(
        action="back_to_main"
    ).pack()


def test_get_contact_keyboard():
    """Tests the get_contact_keyboard function."""
    keyboard = get_contact_keyboard()
    assert isinstance(keyboard, InlineKeyboardMarkup)

    buttons = {btn.text: btn for row in keyboard.inline_keyboard for btn in row}

    assert "GitHub" in buttons
    assert buttons["GitHub"].url == "https://github.com/mynamemyway"
    assert "⬅️ Return" in buttons


def test_get_help_keyboard():
    """Tests the get_help_keyboard function."""
    keyboard = get_help_keyboard()
    assert isinstance(keyboard, InlineKeyboardMarkup)

    buttons = {btn.text: btn for row in keyboard.inline_keyboard for btn in row}

    assert "🔄 Restart" in buttons
    assert buttons["🔄 Restart"].callback_data == MainMenuCallback(
        action="restart_session"
    ).pack()
    assert "🗑️ Clear history" in buttons
    assert buttons["🗑️ Clear history"].callback_data == MainMenuCallback(
        action="reset_chat"
    ).pack()