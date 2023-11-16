from aiogram import Router
from aiogram.types import Message

from app.db.functions import User, Schedule

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

    text = '<pre><code class="language-table">'
    for lesson in day:
        if type(lesson) == list:
            lesson1 = lesson[0] if lesson[0] != None else "Нет пары"
            lesson2 = lesson[1] if lesson[1] != None else "Нет пары"
            text += f"{lesson1} | {lesson2}\n"
        else:
            text += f"{lesson if lesson != None else 'Нет пары'}\n"

    text += "</code></pre>"

    await message.answer(text)
