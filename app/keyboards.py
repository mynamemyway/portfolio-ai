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
    builder.button(text="➡️ Hello world!", callback_data=MainMenuCallback(action="hello"))
    builder.button(text="👋 AI about me", callback_data=MainMenuCallback(action="about_me"))
    builder.button(text="Skills", callback_data=MainMenuCallback(action="skills"))
    builder.button(text="Projects", callback_data=MainMenuCallback(action="projects"))
    builder.button(text="Contacts", callback_data=MainMenuCallback(action="contact"))
    # Arrange the buttons: 1 button in the first row, 2 in the second, 2 in the third.
    builder.adjust(2, 3)
    return builder.as_markup()


def get_hello_world_keyboard() -> InlineKeyboardMarkup:
    """
    Builds and returns an alternative main keyboard for the 'Hello world!' view.

    This keyboard replaces the 'Hello world!' button with a 'back' button to
    return to the initial welcome message, creating a toggle effect.
    """
    builder = InlineKeyboardBuilder()
    # This button returns the user to the initial welcome message.
    builder.button(
        text="⬅️ About bot", callback_data=MainMenuCallback(action="about_portfolio")
    )
    builder.button(text="👋 AI about me", callback_data=MainMenuCallback(action="about_me"))
    builder.button(text="Skills", callback_data=MainMenuCallback(action="skills"))
    builder.button(text="Projects", callback_data=MainMenuCallback(action="projects"))
    builder.button(text="Contacts", callback_data=MainMenuCallback(action="contact"))
    # The layout is identical to the main keyboard for consistency.
    builder.adjust(2, 3)
    return builder.as_markup()


def get_skills_keyboard() -> InlineKeyboardMarkup:
    """
    Builds and returns the skills submenu inline keyboard.

    This keyboard allows the user to choose between viewing hard skills or soft skills.
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Hard skills", callback_data=MainMenuCallback(action="hard_skills")
    )
    builder.button(
        text="Soft skills", callback_data=MainMenuCallback(action="soft_skills")
    )
    builder.button(text="⬅️ Return", callback_data=MainMenuCallback(action="back_to_main"))
    builder.adjust(2, 1)
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
    builder.button(
        text="Tell about Portfolio AI",
        callback_data=MainMenuCallback(action="show_project_portfolio_ai"),
    )
    builder.button(text="Portfolio AI on Git", url="https://github.com/mynamemyway/portfolio-ai")
    builder.button(text="⬅️ Return", callback_data=MainMenuCallback(action="back_to_main"))
    # Arrange the buttons: each on a new line for better readability.
    builder.adjust(1, 1, 1, 1, 1)
    return builder.as_markup()


def get_help_keyboard() -> InlineKeyboardMarkup:
    """
    Builds and returns the inline keyboard for the /help command message.

    This keyboard provides users with quick actions to restart the session,
    clear their chat history, and contact you directly.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="Telegram", url="https://t.me/mynamemyway")
    builder.button(
        text="🗑️ Clear history", callback_data=MainMenuCallback(action="reset_chat")
    )
    builder.button(
        text="🔄 Restart",
        callback_data=MainMenuCallback(action="restart_session"),
    )
    builder.button(text="⬅️ Return", callback_data=MainMenuCallback(action="back_to_main"))
    builder.adjust(2, 2)
    return builder.as_markup()