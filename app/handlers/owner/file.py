from aiogram import F
from aiogram import Router
from aiogram.types import Message

from app.db.functions import Schedule, Group
from app.utils.formatter import excel_to_schedule
import xlrd, os

from app.filters.is_owner import IsOwner

router = Router()


@router.message(IsOwner(is_owner=True), F.content_type.in_({"document", "image"}))
async def file_handler(message: Message):
    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)

    await message.bot.download_file(file.file_path, "file.xls")

    excel = xlrd.open_workbook("file.xls")
    sheet = excel.sheet_by_index(0)

    table = []

    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        table.append(row)

    schedule = await excel_to_schedule(table)

    if await Group.group_exists(schedule["group"]):
        await Schedule.edit_schedule(
            group=schedule["group"],
            lessons=schedule["lessons"],
        )
        await message.answer("Расписание успешно обновлено!")
    else:
        await Group.create_group(schedule["group"])

        await Schedule.create(
            group=schedule["group"],
            lessons=schedule["lessons"],
        )
        await message.answer("Расписание и группа успешно добавлены!")

    os.remove("file.xls")
