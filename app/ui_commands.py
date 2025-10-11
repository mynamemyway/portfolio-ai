# app/ui_commands.py

from aiogram import Bot
from aiogram.types import BotCommand


async def set_ui_commands(bot: Bot):
    """
    Sets the UI commands for the bot in the Telegram menu.

    These commands provide users with quick access to the bot's main features.
    """
    commands = [
        BotCommand(command="start", description="restart"),
        BotCommand(command="help", description="info & help"),
        BotCommand(command="reset", description="clear history"),
    ]
    await bot.set_my_commands(commands=commands)