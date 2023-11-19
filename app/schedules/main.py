import asyncio
import aioschedule
import logging

from app.db.functions import User, Schedule
from app.utils.formatter import format_schedule
from datetime import datetime, timedelta

from aiogram import Bot


async def scheduler(bot: Bot):
    logging.info("Running background worker")
    aioschedule.every().day.at("15:00").do(main_schedule, bot=bot)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(3)


async def main_schedule(bot: Bot):
    logging.info("Running main schedule")
    # send next day schedule
    now = datetime.now().weekday()

    if now == 5:
        return
    elif now == 6:
        now = 0
    else:
        now += 1

    sended = 0

    users = await User.all()
    for user in users:
        try:
            if user.group:
                lessons = (await Schedule.get_schedule(user.group)).lessons
                day = lessons[now]
                text = "Расписание на завтра:\n\n" + await format_schedule(day)

                await bot.send_message(
                    user.telegram_id,
                    text,
                )
                sended += 1
        except Exception:
            pass

    logging.info(f"Sended {sended} messages")
