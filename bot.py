import asyncio
import logging
from config import token

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from menu import register_handlers_order
from common import register_handlers_common

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/order", description="Заказать кальян"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")


    bot = Bot(token = token)
    dp = Dispatcher(bot, storage = MemoryStorage())

    register_handlers_common(dp)
    register_handlers_order(dp)

    await set_commands(bot)

    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())