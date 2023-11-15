from aiogram import Router


def get_dialog_router() -> Router:
    from .choice_group import ui

    dialog_routers = Router()

    dialog_routers.include_router(ui)

    return dialog_routers
