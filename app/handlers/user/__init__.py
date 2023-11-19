from aiogram import Router


def get_user_router() -> Router:
    from . import info, group, start, text, file

    router = Router()
    router.include_router(info.router)
    router.include_router(group.router)
    router.include_router(start.router)
    router.include_router(file.router)
    router.include_router(text.router)

    return router
