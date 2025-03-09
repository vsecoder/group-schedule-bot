import asyncio
import aioschedule
import logging
from datetime import datetime, date

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from app.db.functions import User
from app.utils.formatter import format_schedule

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
    current_week = (date.today().isocalendar()[1]) % 2

    if now == 5:
        return
    if now == 6:
        current_week += 1
        now = 0
    else:
        now += 1

    week_type = "числитель" if current_week == 0 else "знаменатель"

    sent_count = 0
    users = await User.all().prefetch_related("group")

    for user in users:
        if not user.group:
            continue

        try:
            lessons = await User.get_final_schedule(
                user.telegram_id, date.today(), now, week_type
            )

            if not lessons:
                continue

            days = ["пн", "вт", "ср", "чт", "пт", "сб"]
            text = await format_schedule(lessons, days[now], week_type)

            await bot.send_message(user.telegram_id, text)
            sent_count += 1
        except TelegramAPIError:
            pass

    logger.info(f"Отправлено {sent_count} сообщений")
