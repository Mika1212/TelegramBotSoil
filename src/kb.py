from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

menu = [
    [InlineKeyboardButton(text="📸 Отправить фото", callback_data="send_photo"),
     InlineKeyboardButton(text="🔎 Инструкция", callback_data="instruction")],
    [InlineKeyboardButton(text="📝 Связаться с нами", callback_data="message_us"),
     InlineKeyboardButton(text="❓ Как это работает", callback_data="how_it_works")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
