import asyncio
import aioschedule
import logging

from app.db.functions import User, Schedule
from app.utils.formatter import format_schedule
from datetime import datetime

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

logger = logging.getLogger(__name__)


async def scheduler(bot: Bot) -> None:
    """Run background worker"""
    logger.info("Running background worker")
    aioschedule.every().day.at("15:00").do(main_schedule, bot=bot)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(3)


async def main_schedule(bot: Bot) -> None:
    """Send schedule to all users"""
    logger.info("Running main schedule")

    now = datetime.now().weekday()

    if now == 5:
        return

    if now == 6:
        now = 0
    else:
        now += 1

    sended = 0

    users = await User.all()
    for user in users:
        try:
            if user.group:
                lessons = await Schedule.get_schedule(user.group)

                if not lessons:
                    continue

                lessons = lessons.lessons
                day = lessons[now]
                days = ["пн", "вт", "ср", "чт", "пт", "сб"]
                text = await format_schedule(day, days[now], "числителю / знаменателю")

                await bot.send_message(
                    user.telegram_id,
                    text,
                )
                sended += 1
        except TelegramAPIError:
            pass

    logger.info(f"Sended {sended} messages")
