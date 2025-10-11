# app/ui_commands.py

from aiogram import Bot
from aiogram.types import BotCommand


async def set_ui_commands(bot: Bot):
    """
    Sets the UI commands for the bot in the Telegram menu.

    These commands provide users with quick access to the bot's main features.
    """
    commands = [
        BotCommand(command="start", description="Reboot"),
        BotCommand(command="help", description="Help & info"),
    ]
    await bot.set_my_commands(commands=commands)