from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    confirm_sending_mail = State()
    message_us_question = State()
    send_photo = State()
    message_us_mail = State()
    main_menu = State()
    send_mail = State()