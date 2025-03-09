import os
from aiogram import F
from aiogram import Router
from aiogram.types import Message

from app.utils.formatter import excel_to_schedule

from app.filters.is_owner import IsOwner

router = Router()


@router.message(IsOwner(is_owner=True), F.content_type.in_({"document", "image"}))
async def file_handler(message: Message):
    """Catch file, need to update schedule (later lesson replacements)"""
    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)

    await message.bot.download_file(file.file_path, "file.xls")

    await excel_to_schedule("file.xls")
    await message.answer("Расписание и группа успешно добавлены!")

    os.remove("file.xls")
