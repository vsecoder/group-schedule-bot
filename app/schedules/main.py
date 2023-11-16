import asyncio
import aioschedule
import logging

from app.db.functions import User, Schedule
from datetime import datetime, timedelta

# from app.api.server import API

from aiogram import Bot


async def scheduler(bot: Bot):
    logging.info("Running background worker")
    aioschedule.every().day.at("17:00").do(main_schedule, bot=bot)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(3)


async def main_schedule(bot: Bot):
    logging.info("Running main schedule")
    # send next day schedule
    now = datetime.now().weekday()

    if now == 5:
        return
    now += 1

    users = await User.all()
    for user in users:
        if user.group:
            lessons = (await Schedule.get_schedule(user.group)).lessons
            day = lessons[now]
            text = "Расписание на завтра:\n\n"

            for lesson in day:
                if type(lesson) == list:
                    lesson1 = lesson[0] if lesson[0] != None else "Нет пары"
                    lesson2 = lesson[1] if lesson[1] != None else "Нет пары"
                    text += f"{lesson1} | {lesson2}\n"
                else:
                    text += f"{lesson if lesson != None else 'Нет пары'}\n"

            await bot.send_message(
                user.telegram_id,
                text,
            )
