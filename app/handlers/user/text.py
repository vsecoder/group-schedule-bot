from aiogram import Router
from aiogram.types import Message

from app.db.functions import User, Schedule
from app.utils.formatter import format_schedule

from app.filters.is_registered import IsRegistered

router = Router()


@router.message(IsRegistered(False))
async def not_registered_handler(message: Message):
    """If user not registered, send this message"""
    await message.answer(
        "По какой-то причине вы не зарегистрированы в боте, введите /start"
    )


@router.message()
async def text_handler(message: Message):
    """If user send text message, check if it is day of week"""
    days = {
        "Пн": 0,
        "Вт": 1,
        "Ср": 2,
        "Чт": 3,
        "Пт": 4,
        "Сб": 5,
    }

    if message.text not in days:
        return

    group = (await User.get(telegram_id=message.from_user.id)).group
    if not group:
        await message.answer("Вы не выбрали группу!")
        return

    lessons = (await Schedule.get_schedule(group)).lessons

    day = lessons[days[message.text]]

    text = await format_schedule(day, message.text, "числителю / знаменателю")

    await message.answer(text)
