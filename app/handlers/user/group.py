from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.dialogs.choice_group import GroupDialog

router = Router()


@router.message(Command(commands=["group"]))
async def group_dialog_handler(_: Message, dialog_manager: DialogManager):
    """Start group dialog"""
    await dialog_manager.start(GroupDialog.choice)
