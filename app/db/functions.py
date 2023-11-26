from typing import Union

from tortoise.exceptions import DoesNotExist

from app.db import models


class User(models.User):
    @classmethod
    async def is_registered(cls, telegram_id: int) -> Union[models.User, bool]:
        """
        Check if user is registered

        :param telegram_id: Telegram user id
        :return: User object or False
        """
        try:
            return await cls.get(telegram_id=telegram_id)
        except DoesNotExist:
            return False

    @classmethod
    async def register(cls, telegram_id) -> None:
        """
        Create new user

        :param telegram_id: Telegram user id
        :return: None
        """
        await User(telegram_id=telegram_id).save()

    @classmethod
    async def get_count(cls) -> int:
        """
        Get count of registered users

        :return: Count of registered users
        """
        return await cls.all().count()

    @classmethod
    async def edit_group(cls, telegram_id, group) -> bool:
        """
        Edit user group

        :param telegram_id: Telegram user id
        :param group: New group
        :return: True if group exists, else False
        """
        user = await cls.get(telegram_id=telegram_id)
        user.group = group
        if await Group.group_exists(group):
            await user.save()
            return True
        return False


class Group(models.Group):
    @classmethod
    async def group_exists(cls, group: str) -> bool:
        """
        Check if group exists

        :param group: Group name
        :return: True if group exists, else False
        """
        try:
            await cls.get(name=group)
            return True
        except DoesNotExist:
            return False

    @classmethod
    async def create_group(cls, group: str) -> None:
        """
        Create new group

        :param group: Group name
        :return: None
        """
        await Group(name=group).save()

    @classmethod
    async def get_all_groups(cls) -> list:
        """
        Get all groups

        :return: List of groups
        """
        groups = await cls.all()
        return [group.name for group in groups]


class Schedule(models.Schedule):
    @classmethod
    async def get_schedule(cls, group: str) -> Union[models.Schedule, bool]:
        """
        Get schedule by group

        :param group: Group name
        :return: Schedule object or False
        """
        try:
            return await cls.get(group=group)
        except DoesNotExist:
            return False

    @classmethod
    async def create_schedule(cls, group: str, replacements: dict) -> None:
        """
        Create new schedule

        :param group: Group name
        :param replacements: replacements
        :return: None
        """
        await Schedule(group=group, replacements=replacements).save()

    @classmethod
    async def edit_schedule(cls, group: str, replacements: dict) -> None:
        """
        Edit schedule

        :param group: Group name
        :param replacements: replacements
        :return: None
        """
        schedule = await cls.get(group=group)
        schedule.replacements = replacements
        await schedule.save()


class Replacement(models.Replacement):
    @classmethod
    async def get_replacement(cls, group: str) -> Union[models.Replacement, bool]:
        """
        Get replacement by group

        :param group: Group name
        :return: Replacement object or False
        """
        try:
            return await cls.get(group=group)
        except DoesNotExist:
            return False

    @classmethod
    async def create_replacement(cls, group: str, replacements: dict) -> None:
        """
        Create new replacement

        :param group: Group name
        :param replacements: replacements
        :return: None
        """
        await Replacement(group=group, replacements=replacements).save()

    @classmethod
    async def edit_replacement(cls, group: str, replacements: dict) -> None:
        """
        Edit replacement

        :param group: Group name
        :param replacements: replacements
        :return: None
        """
        replacement = await cls.get(group=group)
        replacement.replacements = replacements
        await replacement.save()
