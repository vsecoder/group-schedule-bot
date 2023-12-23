from tortoise import fields
from tortoise.models import Model

from datetime import datetime


class User(Model):
    id = fields.BigIntField(pk=True, generated=True)
    telegram_id = fields.BigIntField()
    group = fields.CharField(max_length=255, null=True)
    role = fields.CharField(max_length=255, default="user")
    # for statistic later
    date = fields.CharField(max_length=255, default=datetime.now().strftime("%d.%m.%Y"))


class Group(Model):
    id = fields.BigIntField(pk=True, generated=True)
    name = fields.CharField(max_length=255)


class Schedule(Model):
    id = fields.BigIntField(pk=True, generated=True)
    group = fields.CharField(max_length=255)
    lessons = fields.JSONField()


class Replacement(Model):
    id = fields.BigIntField(pk=True, generated=True)
    replacements = fields.JSONField()

    # left or right - чиcлитель или знаменатель
    sequence = fields.CharField(max_length=255, default="left")
