from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.dialogs.choice_group import GroupDialog

router = Router()


@router.message(Command(commands=["group"]))
async def group_dialog_handler(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(GroupDialog.choice)
    """
    П-207 [[null,[null,"эл.высш.мат. - 213"],"инф.технологии - 317","рус.яз и к.р. - 101",[null,"пр. и диз. ИС - л210"]],[null,"ин.яз. - 312/102"],[["осн.алгоритмиз. - л212",null],"эл.высш.мат - 213","физ-ра"],[null,"теор.вер и МС - 304","пр. и диз. ИС - л210"],["арх.аппар.ср-в - 317","дискр.мат. - 318","осн.алгоритмиз - л212"],["осн.алгоритмиз - л212","опер.системы - 318","осн.алгоритмиз - л212"]]
    """

    """
    С-202 [[None, "осн.теор.инф. - 317", "инж.комп.граф - 301/305"],["ин.яз. - 102/312",["проектир.КС - л209", "комп.сети - 318"],"комп.сети - 318",],["комп.сети - 318","электротехн. - 306",["эл.высш.мат - 304", "осн.теор.инф. - 317"],],[None, None, "физ-ра", "эл.высш.мат - 304"],[None,["арх.аппар.ср-в - 317", "проектир.КС - л209"],"арх.аппар.ср-в - 317",],["комп.сети - 318", "дискр.мат. - 213", "рус.яз. и - 315"]]
    """
