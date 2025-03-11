"""Functions for formatting data"""

import pandas as pd
from app.db.functions import Schedule, Group


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


async def format_schedule(
    group_schedule: list, day: str, sequence: str, scheduled: bool = False
) -> str:
    """
    Форматирует расписание в читабельный вид

    :param group_schedule: Список пар на день
    :param day: День недели
    :param sequence: Числитель/Знаменатель
    :param scheduled: Флаг, определяющий, что сообщение из расписания
    :return: Отформатированное расписание
    """
    schedule_text = ""
    time_slots = TIME[0] if day.lower() != "сб" else TIME[1]

    if not group_schedule or group_schedule == [None]:
        return f"✨ Нет пар на {day}"

    schedule_by_slot = {
        lesson["time_slot"]: lesson for lesson in group_schedule if lesson
    }

    for slot, (from_time, to_time) in enumerate(time_slots, start=1):
        lesson_data = schedule_by_slot.get(slot)

        if lesson_data:
            schedule_text += TEMPLATE_LESSON.format(
                number=slot,
                lesson=lesson_data["subject"] or "-",
                from_time=from_time,
                to_time=to_time,
                class_num=lesson_data["classroom"] or "-",
            )
        # else:
        #    schedule_text += TEMPLATE_EMPTY_LESSON.format(
        #        number=slot,
        #        from_time=from_time,
        #        to_time=to_time,
        #    )

    sequence = "числителю" if sequence == "числитель" else "знаменателю"

    return TEMPLATE_SCHEDULE.format(
        day=day if not scheduled else "завтра",
        sequence=sequence, 
        schedule=schedule_text
    )


async def excel_to_schedule(file_path: str) -> None:
    """
    Парсинг Excel-таблицы и сохранение расписания в БД

    :param file_path: Путь к Excel-файлу
    """
    df = pd.read_excel(file_path, header=None)

    group_name = str(df.iloc[0, 0]).strip()
    df = df.iloc[2:].reset_index(drop=True)

    empty_lesson = {"нетпары", "-", "н/б", "", "nan"}
    lessons = [[] for _ in range(6)] 

    await Group.get_or_create_group(group_name)

    for time_slot, row in df.iterrows():
        for day in range(6):
            cell_value = str(row[day]).strip() if pd.notna(row[day]) else ""

            if cell_value.lower().replace(" ", "") in empty_lesson:
                lessons[day].append(None)
                continue

            separated = [part.strip() for part in cell_value.split(" | ")]

            parsed_lessons = [
                None if part.lower().replace(" ", "") in empty_lesson else part
                for part in separated
            ]

            lessons[day].append(
                {
                    "time_slot": time_slot + 1,
                    "week_type": "числитель" if len(parsed_lessons) > 1 else "всегда",
                    "subject": parsed_lessons[0],
                    "classroom": None,
                }
            )

            if len(parsed_lessons) > 1:
                lessons[day].append(
                    {
                        "time_slot": time_slot + 1,
                        "week_type": "знаменатель",
                        "subject": parsed_lessons[1],
                        "classroom": None,
                    }
                )

    await Schedule.update_or_create(group_name=group_name, lessons=lessons)
