from typing import Union

from tortoise.exceptions import DoesNotExist

from app.db import models


class User(models.User):
    @classmethod
    async def is_registered(cls, telegram_id: int) -> Union[models.User, bool]:
        try:
            return await cls.get(telegram_id=telegram_id)
        except DoesNotExist:
            return False

    @classmethod
    async def register(cls, telegram_id) -> None:
        await User(telegram_id=telegram_id).save()

    @classmethod
    async def get_count(cls) -> int:
        return await cls.all().count()

    @classmethod
    async def edit_group(cls, telegram_id, group) -> bool:
        user = await cls.get(telegram_id=telegram_id)
        user.group = group
        if await Group.group_exists(group):
            await user.save()
            return True
        else:
            return False


class Group(models.Group):
    @classmethod
    async def group_exists(cls, group: str) -> bool:
        try:
            await cls.get(name=group)
            return True
        except DoesNotExist:
            return False

    @classmethod
    async def create_group(cls, group: str) -> None:
        await Group(name=group).save()

    @classmethod
    async def get_all_groups(cls) -> list:
        groups = await cls.all()
        return [group.name for group in groups]


class Schedule(models.Schedule):
    @classmethod
    async def get_schedule(cls, group: str) -> Union[models.Schedule, bool]:
        try:
            return await cls.get(group=group)
        except DoesNotExist:
            return False

    @classmethod
    async def create_schedule(cls, group: str, lessons: dict) -> None:
        await Schedule(group=group, lessons=lessons).save()

    @classmethod
    async def edit_schedule(cls, group: str, lessons: dict) -> None:
        schedule = await cls.get(group=group)
        schedule.lessons = lessons
        await schedule.save()
