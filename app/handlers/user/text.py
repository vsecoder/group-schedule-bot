from aiogram import Router
from aiogram.types import Message
from datetime import date

from app.db.functions import User
from app.utils.formatter import format_schedule

from app.filters.is_registered import IsRegistered

router = Router()

DAYS = {
    "Пн": 0,
    "Вт": 1,
    "Ср": 2,
    "Чт": 3,
    "Пт": 4,
    "Сб": 5,
}


@router.message(IsRegistered(False))
async def not_registered_handler(message: Message):
    """Если пользователь не зарегистрирован, отправляем сообщение"""
    await message.answer("Вы не зарегистрированы в боте, введите /start")


@router.message()
async def text_handler(message: Message):
    """Обрабатывает сообщение пользователя, если оно является днем недели"""
    if message.text not in DAYS:
        return

    user = await User.get(telegram_id=message.from_user.id)

    if not user or not user.group:
        await message.answer("Вы не выбрали группу!")
        return

    current_week = (date.today().isocalendar()[1]) % 2
    week_type = "числитель" if current_week == 1 else "знаменатель"

    lessons = await User.get_final_schedule(
        user.telegram_id, date.today(), DAYS[message.text], week_type
    )

    if not lessons:
        await message.answer(f"✨ Нет пар на {message.text}")
        return

    text = await format_schedule(lessons, message.text, week_type)

    await message.answer(text)
