from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram import types

from tgbot.keyboards.reply import menu_replk
from tgbot.states.menustats import MenuStates


# User handlers

async def show_menu(message: types.Message):
    await message.answer("Выберите то, что вашей душе угодно", reply_markup=menu_replk)
    await MenuStates.menu_is_shown.set()


async def close_menu(message: types.Message, state: FSMContext):
    await message.answer("Меню закрыто", reply_markup=types.ReplyKeyboardRemove())
    await state.reset_state()


async def connect_to_support(message: types.Message):
    await message.answer("Напишите ваше сообщение, оно отобразиться у службы поддержки:", reply_markup=types.ReplyKeyboardRemove())
    await MenuStates.message_to_support.set()


async def send_message_to_support(message: types.Message, state: FSMContext, dp: Dispatcher):
    for admin_id in dp.bot.get("config").tg_bot.admin_ids:
        await dp.bot.forward_message(admin_id, message.chat.id, message.message_id, message.text)
    await state.reset_state()


# Admin handlers

async def answer_message(message: types.Message, dp: Dispatcher):

    # await message.reply_to_message.delete()
    # await message.delete()
    
    user_id = message.reply_to_message.forward_from["id"]
    text = message.text
    await dp.bot.send_message(user_id, text)


def register_news(dp: Dispatcher):
    dp.register_message_handler(lambda mes: answer_message(mes, dp), is_reply_forwarded=True)
    dp.register_message_handler(show_menu, commands=["menu"])
    dp.register_message_handler(lambda mes: close_menu(mes, dp.current_state()), 
                                regexp="Закрыть меню",
                                state=MenuStates.menu_is_shown)
    dp.register_message_handler(connect_to_support, 
                                regexp="Написать в поддержку", 
                                state=MenuStates.menu_is_shown)
    dp.register_message_handler(lambda mes: send_message_to_support(mes, dp.current_state(), dp), 
                                state=MenuStates.message_to_support, 
                                content_types=types.ContentTypes.ANY)
