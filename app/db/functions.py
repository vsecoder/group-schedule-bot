from typing import List, Union

from tortoise.exceptions import DoesNotExist
from tortoise.expressions import Q

from app.db import models


class User(models.User):

    @classmethod
    async def is_registered(cls, telegram_id: int) -> Union["User", bool]:
        """Проверяет, зарегистрирован ли пользователь."""
        try:
            return await cls.get(telegram_id=telegram_id)
        except DoesNotExist:
            return False

    @classmethod
    async def register(cls, telegram_id: int) -> None:
        """Создаёт нового пользователя."""
        await cls.create(telegram_id=telegram_id)

    @classmethod
    async def get_count(cls) -> int:
        """Возвращает количество зарегистрированных пользователей."""
        return await cls.all().count()

    @classmethod
    async def edit_group(cls, telegram_id: int, group_name: str) -> bool:
        """
        Изменяет группу пользователя.

        :param telegram_id: Telegram ID пользователя
        :param group_name: Название новой группы
        :return: True, если группа существует и обновлена, иначе False
        """
        user = await cls.get(telegram_id=telegram_id)
        group = await Group.get_or_none(name=group_name)

        if group:
            user.group = group
            await user.save()
            return True
        return False

    @classmethod
    async def get_user_group(cls, telegram_id: int) -> Union[str, None]:
        """Возвращает название группы пользователя, если она назначена."""
        user = await cls.get(telegram_id=telegram_id).prefetch_related("group")
        return user.group.name if user.group else None

    @classmethod
    async def get_schedule(
        cls, telegram_id: int, day_of_week: int, week_type: str
    ) -> List[dict]:
        """
        Получает расписание пользователя на указанный день.

        :param telegram_id: Telegram ID пользователя
        :param day_of_week: День недели (0 - Пн, 1 - Вт, ..., 5 - Сб)
        :param week_type: "numerator" или "denominator"
        :return: Список пар в формате [{ "subject": ..., "classroom": ... }, ...]
        """
        user = await cls.get(telegram_id=telegram_id).prefetch_related("group")
        if not user.group:
            return []

        schedule = await Schedule.filter(
            group=user.group, day_of_week=day_of_week, week_type=week_type
        ).all()
        return [{"subject": s.subject, "classroom": s.classroom} for s in schedule]

    @classmethod
    async def get_replacements(cls, telegram_id: int, date) -> List[dict]:
        """
        Получает разовые замены пользователя на указанную дату.

        :param telegram_id: Telegram ID пользователя
        :param date: Дата замены (формат datetime.date)
        :return: Список замен в формате [{ "subject": ..., "classroom": ..., "time_slot": ... }, ...]
        """
        user = await cls.get(telegram_id=telegram_id).prefetch_related("group")
        if not user.group:
            return []

        replacements = await Replacement.filter(group=user.group, date=date).all()
        return [
            {"subject": r.subject, "classroom": r.classroom, "time_slot": r.time_slot}
            for r in replacements
        ]

    @classmethod
    async def get_final_schedule(
        cls, telegram_id: int, date, day_of_week: int, week_type: str
    ) -> List[dict]:
        """
        Получает итоговое расписание пользователя с учетом замен.

        :param telegram_id: Telegram ID пользователя
        :param date: Дата запроса (формат datetime.date)
        :param day_of_week: День недели (0 - Пн, 1 - Вт, ..., 5 - Сб)
        :param week_type: "numerator" или "denominator"
        :return: Список занятий с заменами, если они есть
        """
        user = await cls.get(telegram_id=telegram_id).prefetch_related("group")
        if not user.group:
            return []

        schedule = await Schedule.filter(
            Q(group_id=user.group.id)
            & Q(day_of_week=day_of_week)
            & (Q(week_type="всегда") | Q(week_type=week_type))
        ).all()
        schedule_dict = {i: {"subject": None, "classroom": None} for i in range(1, 7)}

        for lesson in schedule:
            schedule_dict[lesson.id] = {
                "subject": lesson.subject,
                "classroom": lesson.classroom,
                "time_slot": lesson.time_slot,
            }

        replacements = await Replacement.filter(group=user.group, date=date).all()
        for replacement in replacements:
            schedule_dict[replacement.time_slot] = {
                "subject": replacement.subject,
                "classroom": replacement.classroom,
                "time_slot": replacement.time_slot,
            }

        return [v for v in schedule_dict.values() if v["subject"]]

    @classmethod
    async def add_replacement(
        cls, telegram_id: int, date, subject: str, classroom: str, time_slot: int
    ) -> bool:
        """
        Добавляет разовую замену в расписание пользователя.

        :param telegram_id: Telegram ID пользователя
        :param date: Дата замены (формат datetime.date)
        :param subject: Новый предмет
        :param classroom: Новая аудитория
        :param time_slot: Время пары (1-6)
        :return: True, если успешно добавлено
        """
        user = await cls.get(telegram_id=telegram_id).prefetch_related("group")
        if not user.group:
            return False

        await Replacement.create(
            group=user.group,
            date=date,
            subject=subject,
            classroom=classroom,
            time_slot=time_slot,
        )
        return True


class Group(models.Group):
    @classmethod
    async def get_or_create_group(cls, name: str):
        group, _ = await cls.get_or_create(name=name)
        return group

    @classmethod
    async def get_all_groups(cls):
        return [group.name for group in await cls.all()]


class Schedule(models.Schedule):
    @classmethod
    async def add_schedule(
        cls,
        group_name: str,
        day: int,
        week_type: str,
        time_slot: int,
        subject: str,
        classroom: str = None,
    ):
        """Добавление расписания в БД"""
        group = await Group.get_or_create_group(group_name)
        return await cls.create(
            group=group,
            day_of_week=day,
            week_type=week_type,
            time_slot=time_slot,
            subject=subject,
            classroom=classroom,
        )

    @classmethod
    async def update_or_create(cls, group_name: str, lessons: list) -> None:
        """
        Обновление или создание расписания для группы

        :param group_name: Название группы
        :param lessons: Список расписания (6 дней, пары в день)
        """
        group = await Group.get_or_create_group(group_name)

        await cls.filter(group=group).delete()

        for day, day_lessons in enumerate(lessons):
            schedule_by_slot = {}

            for lesson in day_lessons:
                if lesson is None:
                    continue

                if lesson["subject"] is None:
                    continue

                time_slot = lesson["time_slot"]
                week_type = lesson["week_type"]
                subject, classroom = cls._parse_subject_and_classroom(lesson["subject"])

                schedule_by_slot.setdefault(time_slot, {})[week_type] = {
                    "subject": subject,
                    "classroom": classroom,
                }

            for time_slot, week_data in schedule_by_slot.items():
                for week_type, lesson_data in week_data.items():
                    await cls.create(
                        group=group,
                        day_of_week=day,
                        time_slot=time_slot,
                        week_type=week_type,
                        subject=lesson_data["subject"],
                        classroom=lesson_data["classroom"],
                    )

    @classmethod
    async def get_schedule_for_group(cls, group_name: str, day: int, week_type: str):
        """Получить расписание группы на определенный день и четность недели"""
        group = await Group.get(name=group_name)
        return (
            await cls.filter(group=group, day_of_week=day, week_type=week_type)
            .order_by("time_slot")
            .all()
        )

    @staticmethod
    def _parse_subject_and_classroom(lesson: str):
        """Разделение предмета и кабинета"""
        if lesson is None:
            return None, None

        if " - " not in lesson:
            return lesson, None

        subject, classroom = lesson.split(" - ", 1)
        return subject, classroom


class Replacement(models.Replacement):
    @classmethod
    async def add_replacement(cls, group_name: str, date, subject: str, classroom: str, time_slot: int):
        """Добавить разовую замену"""
        group = await Group.get_or_create_group(group_name)
        return await cls.create(group=group, date=date, subject=subject, classroom=classroom, time_slot=time_slot)

    @classmethod
    async def get_replacements_for_day(cls, group_name: str, date):
        """Получить разовые замены для группы на определенный день"""
        group = await Group.get(name=group_name)
        return await cls.filter(group=group, date=date).all()
