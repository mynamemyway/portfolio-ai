# app/ui_commands.py

from aiogram import Bot
from aiogram.types import BotCommand


async def set_ui_commands(bot: Bot):
    """
    Sets the UI commands for the bot in the Telegram menu.

    These commands provide users with quick access to the bot's main features.
    """
    commands = [
        BotCommand(command="start", description="restart_session"),
        BotCommand(command="help", description="info_&_help"),
        BotCommand(command="reset", description="clear_chat_history"),
    ]
    await bot.set_my_commands(commands=commands)