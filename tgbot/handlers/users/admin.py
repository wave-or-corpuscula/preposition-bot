from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram import types


async def admin_started(message: types.Message, dp: Dispatcher):
    await message.reply("Hello mister Admin!")


async def notify_admins(dp: Dispatcher):
    for admin in dp.bot.get("config").tg_bot.admin_ids:
        await dp.bot.send_message(admin, "Bot started!")


def register_notifications(dp: Dispatcher):
    dp.register_message_handler(lambda mes: admin_started(mes, dp), commands=["start"], state="*", is_admin=True)
