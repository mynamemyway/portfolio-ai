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
    builder.button(text="Hello word!", callback_data=MainMenuCallback(action="hello"))
    builder.button(text="Skills", callback_data=MainMenuCallback(action="skills"))
    builder.button(text="Projects", callback_data=MainMenuCallback(action="projects"))
    builder.button(text="Contacts", callback_data=MainMenuCallback(action="contact"))
    # Arrange the buttons: 1 button in the first row, 3 in the second.
    builder.adjust(1, 3)
    return builder.as_markup()


def get_contact_keyboard() -> InlineKeyboardMarkup:
    """
    Builds and returns the contact information inline keyboard.

    This keyboard provides URL buttons for social profiles and a back button
    to return to the main menu.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="GitHub", url="https://github.com/mynamemyway")
    builder.button(text="Telegram", url="https://t.me/mynamemyway")
    builder.button(text="Instagram", url="https://instagram.com/myname_myway")
    builder.button(text="⬅️ Return", callback_data=MainMenuCallback(action="back_to_main"))
    # Arrange the buttons: 3 links in the first row, 1 back button in the second.
    builder.adjust(3, 1)
    return builder.as_markup()


def get_projects_keyboard() -> InlineKeyboardMarkup:
    """
    Builds and returns the projects submenu inline keyboard.

    This keyboard provides options to learn more about a specific project
    or view its source code.
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Tell about PrimeNetworking",
        callback_data=MainMenuCallback(action="show_project_primenet"),
    )
    builder.button(text="PrimeNetworking on Git", url="https://github.com/mynamemyway/prime-net-docs")
    builder.button(text="Portfolio AI on Git", url="https://github.com/mynamemyway/portfolio-ai")
    builder.button(text="⬅️ Returne", callback_data=MainMenuCallback(action="back_to_main"))
    # Arrange the buttons: each on a new line for better readability.
    builder.adjust(1, 1, 1, 1)
    return builder.as_markup()