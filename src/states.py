from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    send_photo = State()
    message_us = State()
