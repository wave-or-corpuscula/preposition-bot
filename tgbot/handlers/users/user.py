from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram import types


async def start_command(message: types.Message):
    last_name = message.from_user.last_name
    await message.answer("Hello {}{}{}!".format(message.from_user.first_name, 
                                                ("", " ",)[last_name is not None],
                                                ("", last_name,)[last_name is not None]))


def register_user(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["Start"], state="*", is_admin=False)
    