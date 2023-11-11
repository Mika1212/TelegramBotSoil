import telebot
from telebot import types
from Bot_info import bot

back_button_text = "Вернуться в главное меню"
back_button = types.KeyboardButton(back_button_text)
back_keyboard = types.ReplyKeyboardMarkup().add(back_button)

@bot.message_handler(content_types=['text'])
def start(message):
    welcome_text = "Добро пожаловать! Я способен определить плодородность почвы по фотографии. Для этого " \
                   "необходимо сфотографировать почву и отправить фотографию мне.\n" \
                   "Для помощи - напиши /explanations\n" \
                   "Для отправки фото - напиши /photo"
    bot.send_message(message.from_user.id, text=welcome_text)

    if message.text == '/explanations':
        bot.register_next_step_handler(message, give_help)
    elif message.text == "/photo":
        pass


def give_help(message):
    help_text = "help_text_dummy\n" \
                "... /light\n" \
                " /back"
    bot.send_message(message.from_user.id, help_text)
    if message.text == '/light':
        bot.register_next_step_handler(message, light_help, reply_markup=back_keyboard)
    elif message.text == "/back":
        bot.register_next_step_handler(message, start, )


def light_help(message):
    bot.send_message(message.from_user.id, )
    bot.register_next_step_handler(message, reply_markup=back_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "explanation":
        text = "Test_explanation"
        bot.send_message(call.message.chat.id, text)
    elif call.data == "send_photo":
        bot.register_next_step_handler(call.message, reply_markup=back_keyboard)


bot.polling(none_stop=True, interval=0)