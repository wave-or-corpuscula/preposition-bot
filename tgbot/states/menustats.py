from aiogram.dispatcher.filters.state import State, StatesGroup


class MenuStates(StatesGroup):
    menu_is_shown = State()
    message_to_support = State()
    offer_news = State()