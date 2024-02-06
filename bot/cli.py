import asyncio
import logging
from colorama import Fore, init
import asyncpg

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from loader import load_config
from filters.user_exists import UserExists
from handlers.admin.admin_router import admin_router
from handlers.auxiliaries.auxiliary_router import auxiliary_router
from handlers.user.user_router import user_router
from services.admin_services.notify import notify_admins
from services.bot_services.set_cmd import set_commands
from middlewares.db import DatabaseMiddleware

init(autoreset=True)
logger = logging.getLogger(__name__)
config = load_config("bot.ini")


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )  # настройка логера
    print(Fore.GREEN + 'STATUS:', Fore.BLUE + "Starting bot")

    storage = MemoryStorage()

    pool = await asyncpg.create_pool(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host
    )

    # proxy_url = "http://proxy.server:3128" - прокси для pythonanywhere
    bot = Bot(token=config.tg_bot.token, parse_mode='html')  # инициализация бота (передается токен и парсмод)
    dp = Dispatcher(storage=storage)  # инициалтзация диспетчера (передается хранилище)

    # подключение роутеров к диспетчеру
    dp.include_router(admin_router)
    dp.include_router(user_router)
    dp.include_router(auxiliary_router)
    # подключение фильтров и мидлварей
    dp.update.middleware(DatabaseMiddleware(pool))
    user_router.message.filter(UserExists(pool))

    # установка команд бота
    await set_commands(bot, config.tg_bot.admin_id)

    try:
        await notify_admins(config.tg_bot.admin_id, bot)  # уведомление админа о запуске
        await dp.start_polling(bot)  # запуск бота
    finally:
        await dp.storage.close()  # закрытие хранилища
        await pool.close()  # закрытие пула
        await bot.session.close()  # закрытие сессии бота


def cli():
    """Wrapper for command line"""
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


# точка входа
if __name__ == '__main__':
    cli()
