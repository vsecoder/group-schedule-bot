from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.db.functions import User
from app.keyboards.reply import main_menu
from app.dialogs.choice_group import GroupDialog

import logging

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, dialog_manager: DialogManager):
    """
    /start command handler, start main menu
    """
    user_id = message.from_user.id
    text = (
        "👋 Привет!\n"
        "Я - бот, который поможет тебе узнать расписание занятий.\n\n"
        "✍️ Мой разработчик активно работает надо мной, "
        "поэтому я буду улучшаться и развиваться, а узнать как и когда можно тут: @fspo_ogu_changelog."
    )

    if not await User.is_registered(user_id):
        await message.answer(text, reply_markup=await main_menu())
        await User.register(user_id)
        logger.info(f"User {user_id} registered")
        return await dialog_manager.start(GroupDialog.choice)

    await message.answer("Клавиатура открыта!", reply_markup=await main_menu())
