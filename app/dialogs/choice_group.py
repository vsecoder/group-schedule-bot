from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format

from app.db.functions import User, Group
from typing import Any
from operator import itemgetter


class GroupDialog(StatesGroup):
    choice = State()


async def callback(c: CallbackQuery, _: Any, manager: DialogManager, item_id: str):
    groups = await Group.get_all_groups()

    if not await User.is_registered(telegram_id=c.from_user.id):
        await c.answer(
            "Ошибка, попробуйте перезапустить бота", show_alert=True, cache_time=0
        )
        await c.message.delete()
        return await manager.done()

    await User.edit_group(c.message.chat.id, groups[int(item_id)])
    await c.answer("Группа выбрана!", show_alert=True, cache_time=0)
    await c.message.delete()
    await manager.done()


async def close(c: CallbackQuery, _: Any, manager: DialogManager):
    await c.message.delete()
    await manager.done()


async def get_top(**kwargs):
    groups = await Group.get_all_groups()
    parsed = [(group, groups.index(group)) for group in groups]
    return {"groups": parsed}


ui = Dialog(
    Window(
        Const("<b>Выберите группу: </b>"),
        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                items="groups",
                item_id_getter=itemgetter(1),
                on_click=callback,
                id="s_group",
            ),
            width=1,
            height=5,
            id="scroll_with_pager",
        ),
        Button(Const("Закрыть"), id="close", on_click=close),
        state=GroupDialog.choice,
        getter=get_top,
    ),
)
