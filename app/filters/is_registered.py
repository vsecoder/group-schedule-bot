from aiogram import types
from aiogram.filters import Filter

from app.db.functions import User


class IsRegistered(Filter):
    """Check if user is registered"""

    def __init__(self, is_reg: bool) -> None:
        self.is_reg = is_reg

    async def __call__(self, message: types.Message) -> bool:
        return self.is_reg is (
            await User.is_registered(telegram_id=message.from_user.id)
        )
