async def format_schedule(day):
    text = ""

    for lesson in day:
        index = day.index(lesson) + 1
        if type(lesson) == list:
            lesson1 = lesson[0] if lesson[0] != None else "Нет пары"
            lesson2 = lesson[1] if lesson[1] != None else "Нет пары"
            text += f"{index}. {lesson1} | {lesson2}\n"
        else:
            text += f"{index}. {lesson if lesson != None else 'Нет пары'}\n"

    return text
