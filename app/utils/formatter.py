"""Functions for formatting data"""

TEMPLATE_SCHEDULE = """<b>📅 Расписание на {day} (по {sequence}):</b>

{schedule}"""

TEMPLATE_LESSON = """<code>№{number}.</code>
📚 {lesson}
⏰ с <i>{from_time}</i> по <i>{to_time}</i>
🚪 Кабинет {class_num}

"""

TEMPLATE_EMPTY_LESSON = """<code>№{number}.</code>
📚 Нет пары
⏰ с <i>{from_time}</i> по <i>{to_time}</i>

"""

TIME = [
    [  # будни
        ["08:00", "9:35"],
        ["09:45", "11:20"],
        ["11:55", "13:30"],
        ["13:40", "15:15"],
        ["15:25", "17:00"],
        ["17:10", "18:45"],
        ["18:55", "20:30"],
    ],
    [  # суббота
        ["08:00", "9:35"],
        ["09:45", "11:20"],
        ["11:30", "13:05"],
        ["13:15", "14:50"],
        ["15:00", "16:35"],
        ["16:45", "18:20"],
    ],
]


async def format_schedule(group_schedule: list, day: str, sequence: str) -> str:
    """
    Format schedule

    :param day: List of lessons
    :return: Formatted schedule
    """
    schedule = ""
    index = 1
    time = TIME[0] if day != "Сб" else TIME[1]

    if group_schedule == [None]:
        return "✨ Нет пар"

    for lesson in group_schedule:
        data = {
            "lesson": None,
            "from_time": time[index - 1][0],
            "to_time": time[index - 1][1],
            "class_num": "-",
        }
        if lesson is None:
            schedule += TEMPLATE_EMPTY_LESSON.format(
                number=index, from_time=data["from_time"], to_time=data["to_time"]
            )
        else:
            if isinstance(lesson, list):
                classes = [i.split(" - ")[1] if i else "-" for i in lesson]
                lessons = [i.split(" - ")[0] if i else "Нет пары" for i in lesson]
                data["lesson"] = f"{lessons[0]} / {lessons[1]}"
                data["class_num"] = f"{classes[0]} / {classes[1]}"
            else:
                class_num = lesson.split(" - ")[1] if lesson else "-"
                lesson = lesson.split(" - ")[0] if lesson else "Нет пары"
                data["lesson"] = lesson
                data["class_num"] = class_num

            schedule += TEMPLATE_LESSON.format(
                number=index,
                lesson=data["lesson"],
                from_time=data["from_time"],
                to_time=data["to_time"],
                class_num=data["class_num"],
            )

        index += 1

    return TEMPLATE_SCHEDULE.format(day=day, sequence=sequence, schedule=schedule)


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


"""TODO: write this
async def excel_to_replace(excel: list) -> dict:
    \"""
    Convert excel to replace

    :param excel: Excel table
    :return: Replace dict
    \"""
    excel = excel[2:]
    sequence = excel[0][2].replace(" ", "").lower() == "под чертой"
    date = excel[0][3]
    empty_lesson = ["нетпары", "-", "н/б"]

    replaces = [[] for i in range(6)]

    # line have group, lesson number, old lesson, new lesson, classroom
    pass
"""
