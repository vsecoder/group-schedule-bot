import asyncio
import aioschedule
import logging

from app.db.functions import User  # , Hosts, Servers
from datetime import datetime, timedelta

# from app.api.server import API

from aiogram import Bot


async def scheduler(bot: Bot):
    logging.info("Running background worker")
    aioschedule.every().day.at("20:00").do(main_schedule, bot=bot)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(3)


async def main_schedule(bot: Bot):
    logging.info("Running main schedule")
    # send next day schedule
