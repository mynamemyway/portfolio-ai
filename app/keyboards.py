# app/keyboards.py

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MainMenuCallback(CallbackData, prefix="main_menu"):
    """
    CallbackData factory for main menu buttons.

    This class standardizes the callback data format for the main menu,
    allowing for easy filtering and handling of button presses.

    Attributes:
        action (str): The specific action associated with the button (e.g., 'skills').
    """
    action: str


def get_main_keyboard() -> InlineKeyboardMarkup:
    """
    Builds and returns the main inline keyboard markup.

    This keyboard provides users with primary navigation options.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="Навыки", callback_data=MainMenuCallback(action="skills"))
    builder.button(text="Проекты", callback_data=MainMenuCallback(action="projects"))
    builder.button(text="Контакты", callback_data=MainMenuCallback(action="contact"))
    # Arrange the buttons in a single row with 3 buttons.
    builder.adjust(3)
    return builder.as_markup()


def get_contact_keyboard() -> InlineKeyboardMarkup:
    """
    Builds and returns the contact information inline keyboard.

    This keyboard provides URL buttons for social profiles and a back button
    to return to the main menu.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="MyGitHub", url="https://github.com/mynamemyway")
    builder.button(text="Telegram", url="https://t.me/mynamemyway")
    builder.button(text="Instagram", url="https://instagram.com/myname_myway")
    builder.button(text="⬅️ Назад", callback_data=MainMenuCallback(action="back_to_main"))
    # Arrange the buttons: 3 links in the first row, 1 back button in the second.
    builder.adjust(3, 1)
    return builder.as_markup()