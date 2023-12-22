import os

from aiogram import F, Router, types, flags, Bot
from aiogram.filters import Command

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src import utils
from src.config import bot, server_url
from states import States
import requests

import kb
import text

router = Router()
global counter
counter = 1


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet_text.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.message(States.main_menu)
@router.message(F.text == "Меню")
@router.message(F.text == "меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    print(msg.from_user.id)
    await msg.answer(text.menu_text, reply_markup=kb.menu)


@router.callback_query(F.data == "how_it_works")
async def how_it_works(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.edit_text(text.how_it_works_text)
    await clbck.message.answer(text.exit_text, reply_markup=kb.exit_kb)


@router.callback_query(F.data == "message_us")
async def message_us(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(States.message_us_question)
    await clbck.message.edit_text(text.message_us_text)
    await clbck.message.answer(text.exit_text, reply_markup=kb.exit_kb)


@router.message(States.message_us_question)
@flags.chat_action("typing")
async def message_us_question(msg: Message, state: FSMContext):
    await state.update_data(question=msg.text)
    await msg.answer(text.mail_text, reply_markup=kb.exit_kb)
    await state.set_state(States.message_us_mail)


@router.message(States.message_us_mail)
@flags.chat_action("typing")
async def message_us_mail(msg: Message, state: FSMContext):
    if utils.message_is_mail(msg.text):
        await state.update_data(mail=msg.text)
        user_data = await state.get_data()
        question = user_data['question']
        await msg.answer(text.question_all_text.format(question=question, mail=msg.text),
                         parse_mode='HTML', reply_markup=kb.yes_no_kb)
        await state.set_state(States.confirm_sending_mail)
    else:
        await msg.answer(text="Введи свою почту в верном формате!")


@router.callback_query(F.data == "mail_yes")
async def mail_yes(clbck: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    mail = user_data['mail']
    question = user_data['question']
    if utils.send_mail(question, mail) == 0:
        await clbck.message.answer(text="Письмо отправлено!", reply_markup=kb.exit_kb)
    else:
        await clbck.message.answer(text=text.error_text, reply_markup=kb.exit_kb)


@router.callback_query(F.data == "mail_no")
async def mail_no(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text="Твое письмо не отправлено!", reply_markup=kb.exit_kb)


@router.callback_query(F.data == "instruction")
async def instruction(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.edit_text(text.instruction_text)
    await clbck.message.answer(text.exit_text, reply_markup=kb.exit_kb)


@router.callback_query(F.data == "send_photo")
async def send_photo(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(States.send_photo)
    await clbck.message.edit_text(text.send_photo_text)
    await clbck.message.answer(text.exit_text, reply_markup=kb.exit_kb)


@router.message(States.send_photo)
@flags.chat_action("typing")
async def handle_photo(msg: Message, state: FSMContext):
    global counter

    try:
        file_id = msg.document.file_id
    except:
        file_id = msg.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    CHAT_ID = msg.chat.id
    file_name = F"{CHAT_ID}%{counter}"

    await bot.download_file(file_path, F"Python_server/photos/{file_name}.jpg")
    await msg.answer(text.file_answer_text.format(counter=counter))

    f = open(F"Python_server/photos/{file_name}.jpg", 'rb')
    files = {"file": (f.name, f, "multipart/form-data")}
    requests.post(url=F"{server_url}/download_photo", files=files)
    f.close()
    os.remove(F"Python_server/photos/{file_name}.jpg")

    counter += 1
