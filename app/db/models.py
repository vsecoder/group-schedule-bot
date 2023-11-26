from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True)
    telegram_id = fields.BigIntField()
    group = fields.CharField(max_length=255, null=True)
    role = fields.CharField(max_length=255, default="user")
    # for statistic later
    date = fields.DatetimeField(auto_now_add=True)


class Group(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255)


class Schedule(Model):
    id = fields.BigIntField(pk=True)
    group = fields.CharField(max_length=255)
    lessons = fields.JSONField()


class Replacement(Model):
    id = fields.BigIntField(pk=True)
    replacements = fields.JSONField()
