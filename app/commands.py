from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from app.config import Config

users_commands = {
    "start": "Обновить данные и клавиатуру",
    "help": "Показать список команд",
    "about": "Показать информацию о боте",
    "group": "Выбрать группу",
}

owner_commands = {
    **users_commands,
    "ping": "Check bot ping",
    "stats": "Show bot stats",
    "mail": "Send mail to all users",
}


async def setup_bot_commands(bot: Bot, config: Config) -> None:
    """Setup bot commands"""
    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in owner_commands.items()
        ],
        scope=BotCommandScopeChat(chat_id=config.settings.owner_id),
    )

    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in users_commands.items()
        ],
        scope=BotCommandScopeDefault(),
    )


async def remove_bot_commands(bot: Bot, config: Config) -> None:
    """Remove bot commands"""
    await bot.delete_my_commands(scope=BotCommandScopeDefault())
    await bot.delete_my_commands(
        scope=BotCommandScopeChat(chat_id=config.settings.owner_id)
    )
