from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.commands import owner_commands, users_commands
from app.config import Config
from app.keyboards.inline import get_author_keyboard

from datetime import datetime

router = Router()


@router.message(Command(commands=["help"]))
async def help_handler(message: Message, config: Config):
    text = "ℹ️ <b>Список команд:</b> \n\n"
    commands = (
        owner_commands.items()
        if message.from_user.id == config.settings.owner_id
        else users_commands.items()
    )
    for command, description in commands:
        text += f"/{command} - <b>{description}</b> \n"
    await message.answer(text)


@router.message(Command(commands=["about"]))
async def about_handler(message: Message, config: Config, build, upd, start_time):
    link = "https://github.com/vsecoder/group-schedule-bot"
    text = f"🗓 <b>group-schedule-bot</b> - <a href='{link}'>GitHub</a>\n\n"
    text += f"<b>💫 Version:</b> {upd} #{build[:7]}\n"
    text += f"<b>⌛️ Uptime:</b> {datetime.now() - start_time}"

    await message.answer(
        text,
        reply_markup=get_author_keyboard(config.settings.owner_id),
        disable_web_page_preview=True,
    )
