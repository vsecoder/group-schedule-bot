from aiogram import Router


def get_user_router() -> Router:
    from . import info, now, start, text

    router = Router()
    router.include_router(info.router)
    router.include_router(now.router)
    router.include_router(start.router)
    router.include_router(text.router)

    return router
