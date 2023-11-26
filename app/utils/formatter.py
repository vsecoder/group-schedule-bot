"""Functions for formatting data"""


async def format_schedule(day: list) -> str:
    """
    Format schedule

    :param day: List of lessons
    :return: Formatted schedule
    """
    text = ""
    index = 1

    if day == [None]:
        return "Нет пар"

    for lesson in day:
        if type(lesson) is list:
            lesson1 = lesson[0] if lesson[0] else "Нет пары"
            lesson2 = lesson[1] if lesson[1] else "Нет пары"
            text += f"{index}. {lesson1} | {lesson2}\n"
        else:
            text += f"{index}. {lesson if lesson else 'Нет пары'}\n"

        index += 1

    return text


async def excel_to_schedule(excel: list) -> dict:
    """
    Convert excel to schedule

    :param excel: Excel table
    :return: Schedule dict
    """
    group = excel[0][0]
    excel = excel[2:]
    empty_lesson = ["нетпары", "-", "н/б"]

    lessons = [[] for i in range(6)]

    for day in excel:
        for i in range(6):
            if not day[i]:
                continue
            if day[i].lower().replace(" ", "") in empty_lesson:
                lessons[i].append(None)
            else:
                lessons[i].append(day[i])

    return {
        "group": group,
        "lessons": lessons,
    }


async def get_excel_type(first: str) -> str:
    """
    Get excel type

    :param excel: Excel file
    :return: Excel type
    """

    if first.lower() == "замены":
        return "replacements"
    else:
        return "schedule"


async def excel_to_replace(excel: list) -> dict:
    """
    Convert excel to replace

    :param excel: Excel table
    :return: Replace dict
    """
    excel = excel[2:]
    sequence = excel[0][2].replace(" ", "").lower() == "под чертой"
    date = excel[0][3]
    empty_lesson = ["нетпары", "-", "н/б"]

    replaces = [[] for i in range(6)]

    # line have group, lesson number, old lesson, new lesson, classroom
