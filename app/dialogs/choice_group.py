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


async def callback(
    c: CallbackQuery, _: Any, manager: DialogManager, item_id: str
) -> None:
    """Обработчик выбора группы"""
    user_id = c.from_user.id

    if not await User.is_registered(telegram_id=user_id):
        await c.answer(
            "Ошибка, попробуйте перезапустить бота", show_alert=True, cache_time=0
        )
        await c.message.delete()
        return await manager.done()

    groups = await Group.get_all_groups()

    try:
        selected_group = groups[int(item_id)]
    except (IndexError, ValueError):
        await c.answer("Ошибка при выборе группы!", show_alert=True, cache_time=0)
        return

    await User.edit_group(user_id, selected_group)
    await c.answer(
        f"Вы выбрали группу: {selected_group}!", show_alert=True, cache_time=0
    )
    await c.message.delete()
    await manager.done()


async def close(c: CallbackQuery, _: Any, manager: DialogManager) -> None:
    """Закрытие диалога"""
    await c.message.delete()
    await manager.done()


async def get_top(**kwargs) -> dict:
    """Получает все группы и форматирует их для списка"""
    groups = await Group.get_all_groups()
    return {"groups": list(enumerate(groups))}


ui = Dialog(
    Window(
        Const("<b>Выберите группу: </b>\n"),
        Const("Не хватает вашей группы? "),
        Const(
            "<a href='https://telegra.ph/Ne-hvataet-raspisaniya-vashej-gruppy-03-09'>Прочтите</a>"
        ),
        ScrollingGroup(
            Select(
                Format("{item[1]}"),
                items="groups",
                item_id_getter=itemgetter(0),
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
        disable_web_page_preview=True,
    ),
)
