from aiogram import types


async def main_menu():
    buttons = [
        [
            types.KeyboardButton(text="Пн"),
            types.KeyboardButton(text="Вт"),
            types.KeyboardButton(text="Ср"),
            types.KeyboardButton(text="Чт"),
            types.KeyboardButton(text="Пт"),
            types.KeyboardButton(text="Сб"),
        ],
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard
