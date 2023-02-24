import asyncio

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config

from tgbot.handlers.users.echo import register_echo
from tgbot.handlers.users.admin import register_notifications, notify_admins
from tgbot.handlers.users.news import register_news
from tgbot.handlers.users.user import register_user

from tgbot.filters.admin import AdminFilter
from tgbot.filters.support_answer import ReplyToBot
from tgbot.filters.isreplyforwarded import IsReplyForwarded


async def starup_task(dp: Dispatcher):
    await notify_admins(dp)


def register_all_handlers(dp):
    register_news(dp)
    register_user(dp)
    register_notifications(dp)
    register_echo(dp)


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(ReplyToBot)
    dp.filters_factory.bind(IsReplyForwarded)


async def main():
    config = load_config(".env")
    
    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(bot, storage=storage)

    bot["config"] = config

    register_all_filters(dp)
    register_all_handlers(dp)

    try: 
        await starup_task(dp)
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")
