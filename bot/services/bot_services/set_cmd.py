from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat


async def set_user_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command='/start', description='Начать. Запустить бота.'),
        BotCommand(command='/help', description='Получить помощь.'),
    ]
    scope = BotCommandScopeDefault(type='default')
    await bot.set_my_commands(commands=commands, scope=scope)


async def set_admin_commands(bot: Bot, admin_id: str) -> None:
    commands = [
        BotCommand(command='/help', description='Получить помощь'),
        BotCommand(command='/stat', description='Статистика бота.'),
        BotCommand(command='/id', description='Статистика бота.'),
    ]
    scope = BotCommandScopeChat(type='chat', chat_id=admin_id)
    await bot.set_my_commands(commands=commands, scope=scope)


async def set_commands(bot: Bot, admin_id: str) -> None:
    await set_user_commands(bot)
    await set_admin_commands(bot, admin_id)
