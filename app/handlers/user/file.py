from aiogram import F
from aiogram import Router
from aiogram.types import Message

from app.db.functions import User, Schedule
import logging
import xlrd

router = Router()


@router.message(F.content_type.in_({"document", "image"}))
async def file_handler(message: Message):
    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)

    await message.bot.download_file(file.file_path, "file.xlsx")

    excel = xlrd.open_workbook("file.xlsx")
    sheet = excel.sheet_by_index(0)

    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        print(row)
