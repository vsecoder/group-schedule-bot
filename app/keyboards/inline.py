from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def get_author_keyboard(owner_id) -> InlineKeyboardMarkup:
    """
    Get keyboard with author button
    """
    buttons = [
        [InlineKeyboardButton(text="Автор", url=f"tg://user?id={owner_id}")],
    ]
    keyboard = InlineKeyboardBuilder(markup=buttons)
    return keyboard.as_markup()
