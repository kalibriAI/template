from aiogram import Bot


async def notify_admins(admin_id: str, bot: Bot) -> None:
    await bot.send_message(
        chat_id=admin_id,
        text='Hi Administrator, the Bot started successfully!'
    )
