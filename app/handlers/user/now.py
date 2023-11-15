from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.db.functions import User, Schedule

from datetime import datetime

router = Router()


@router.message(Command(commands=["now"]))
async def support_handler(message: Message):
    lessons = (await Schedule.get_schedule("П-207")).lessons
    """
    [[null,[null,"эл.высш.мат. - 213"],"инф.технологии - 317","рус.яз и к.р. - 101",[null,"пр. и диз. ИС - л210"]],[null,"ин.яз. - 312/102"],[["осн.алгоритмиз. - л212",null],"эл.высш.мат - 213","физ-ра"],[null,"теор.вер и МС - 304","пр. и диз. ИС - л210"],["арх.аппар.ср-в - 317","дискр.мат. - 318","осн.алгоритмиз - л212"],["осн.алгоритмиз - л212","опер.системы - 318","осн.алгоритмиз - л212"]]
    """

    now = datetime.now().weekday()
    text = "Расписание на сегодня:\n\n"
    day = lessons[now]

    for lesson in day:
        if type(lesson) == list:
            lesson1 = lesson[0] if lesson[0] != None else "Нет пары"
            lesson2 = lesson[1] if lesson[1] != None else "Нет пары"
            text += f"{lesson1} | {lesson2}\n"
        else:
            text += f"{lesson if lesson != None else 'Нет пары'}\n"

    await message.answer(text)
