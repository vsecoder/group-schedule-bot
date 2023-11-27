from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.exceptions import TelegramAPIError

from app.filters.is_owner import IsOwner
from app.db.functions import User

import logging

router = Router()

logger = logging.getLogger(__name__)


@router.message(IsOwner(is_owner=True), Command(commands=["mail"]))
async def mail_handler(message: Message, bot: Bot):
    """Mailing to all users"""
    users = await User.all()
    geted = 0
    text = message.text.split(maxsplit=1)[1]

    logger.info(f"Start mailing to {len(users)} users")
    await message.answer(f"✅ Рассылка начата! Всего: {len(users)}")

    for user in users:
        try:
            await bot.send_message(
                user.telegram_id, text, disable_web_page_preview=True, parse_mode="HTML"
            )
            geted += 1
        except TelegramAPIError:
            pass

    logger.info(f"Geted {geted} messages")
    await message.answer(f"✅ Рассылка завершена! Получили: {geted}")
