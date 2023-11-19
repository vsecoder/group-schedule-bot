from aiogram import Router
from aiogram.types import Message

from app.db.functions import User, Schedule
from app.utils.formatter import format_schedule

router = Router()


@router.message()
async def text_handler(message: Message):
    days = {
        "Пн": 0,
        "Вт": 1,
        "Ср": 2,
        "Чт": 3,
        "Пт": 4,
        "Сб": 5,
    }

    if not message.text in days:
        return

    group = (await User.get(telegram_id=message.from_user.id)).group
    if not group:
        await message.answer("Вы не выбрали группу!")
        return

    lessons = (await Schedule.get_schedule(group)).lessons

    day = lessons[days[message.text]]

    text = await format_schedule(day)

    await message.answer(text)
