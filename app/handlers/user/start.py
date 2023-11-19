from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.db.functions import User
from app.keyboards.reply import main_menu
from app.dialogs.choice_group import GroupDialog

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, dialog_manager: DialogManager):
    user_id = message.from_user.id
    text = (
        "👋 Привет!  [beta]\n\n"
        "Я бот, который поможет тебе узнать расписание занятий.\n"
        "Нет из планируемого: делений на числитель и знаменатель, замен (но не точно что будут), всех групп."
    )

    if not await User.is_registered(user_id):
        await message.answer(text, reply_markup=await main_menu())
        await User.register(user_id)
        return await dialog_manager.start(GroupDialog.choice)

    await message.answer("Клавиатура открыта!", reply_markup=await main_menu())
