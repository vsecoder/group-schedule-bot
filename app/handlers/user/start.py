from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.db.functions import User
from app.keyboards.reply import main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    text = (
        "Привет!\n\n"
        "Я бот, который поможет тебе узнать расписание занятий.\n"
        "Бот в бете, пока есть только кнопки дней недель\n"
        "Нет из планируемого: только одна группа(П-207), автоматических уведомлений, делений на числитель и знаменатель, замен (но не точно что будут)."
    )
    if not await User.is_registered(user_id):
        await User.register(user_id)

    await message.answer(text, reply_markup=await main_menu())
