from tortoise import fields
from tortoise.models import Model

from datetime import datetime


class User(Model):
    id = fields.BigIntField(pk=True, generated=True)
    telegram_id = fields.BigIntField(unique=True)
    group = fields.ForeignKeyField(
        "models.Group", related_name="users", null=True
    )
    role = fields.CharField(
        max_length=255, default="user"
    )
    date = fields.CharField(
        max_length=255, default=datetime.now().strftime("%d.%m.%Y")
    )


class Group(Model):
    id = fields.BigIntField(pk=True, generated=True)
    name = fields.CharField(max_length=255)

    schedules: fields.ReverseRelation["Schedule"]


class Schedule(Model):
    id = fields.IntField(pk=True)
    group = fields.ForeignKeyField("models.Group", related_name="schedules")
    day_of_week = fields.IntField()
    week_type = fields.CharField(
        max_length=12
    )
    subject = fields.CharField(max_length=255)
    time_slot = fields.IntField()
    classroom = fields.CharField(
        max_length=10, null=True
    )


class Replacement(Model):
    id = fields.IntField(pk=True)
    group = fields.ForeignKeyField("models.Group", related_name="replacements")
    date = fields.DateField()
    subject = fields.CharField(max_length=255)
    classroom = fields.CharField(max_length=10, null=True)
    time_slot = fields.IntField()
