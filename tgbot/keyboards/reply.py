from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_replk = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("Пердложить новость"),
            KeyboardButton("Написать в поддержку"),
        ],
        [
            KeyboardButton("Закрыть меню"),
        ]
    ],
    resize_keyboard=True
)