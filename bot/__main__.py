import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.handlers.private.admin import admin_router
from bot.handlers.private.left_user import left_user_router
from bot.handlers.private.exceptions import exceptions_private_router
from bot.handlers.channel.join_member import join_router
from bot.handlers.channel.bot_chat_member import bot_channel_member_router
from bot.handlers.channel.update_member import update_router
from bot.handlers.channel.join_defender import defender_router

from bot.db.base import Base
from bot.middlewares.repo import Repository

from bot.config_reader import config


logger = logging.getLogger(__name__)



async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        stream=sys.stdout)

    logger.info("Starting bot")

    bot = Bot(config.bot_token, parse_mode="HTML")
    storage = MemoryStorage()

    engine = create_async_engine(f"{config.db_url}",
                                 future=True, echo=False)

    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    dp = Dispatcher(storage=storage)

    """private routers"""
    left_user_router.message.outer_middleware(Repository(async_session=async_session))
    exceptions_private_router.message.outer_middleware(Repository(async_session=async_session))
    admin_router.message.outer_middleware(Repository(async_session=async_session))
    admin_router.callback_query.outer_middleware(Repository(async_session=async_session))

    """channel routers"""
    join_router.chat_join_request.outer_middleware(Repository(async_session=async_session))
    join_router.chat_member.outer_middleware(Repository(async_session=async_session))
    update_router.chat_member.outer_middleware(Repository(async_session=async_session))
    defender_router.chat_member.outer_middleware(Repository(async_session=async_session))

    """private: admin - leftuser - ex??eptions"""
    dp.include_router(admin_router)
    dp.include_router(left_user_router)
    dp.include_router(exceptions_private_router)

    """channel: botchannelmember - join - defender - update"""
    dp.include_router(bot_channel_member_router)
    dp.include_router(join_router)
    dp.include_router(defender_router)
    dp.include_router(update_router)

    try:
        await bot.get_updates(offset=-1)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        pass


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Exit")
