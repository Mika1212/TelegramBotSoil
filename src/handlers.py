from aiogram import F, Router, types, flags, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.config import bot
from states import States

import kb
import text

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet_text.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.message(F.text == "Меню")
@router.message(F.text == "меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu_text, reply_markup=kb.menu)


@router.callback_query(F.data == "how_it_works")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.edit_text(text.how_it_works_text)
    await clbck.message.answer(text.exit_text, reply_markup=kb.exit_kb)


@router.callback_query(F.data == "message_us")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(States.message_us)
    await clbck.message.edit_text(text.message_us_text)
    await clbck.message.answer(text.exit_text, reply_markup=kb.exit_kb)


@router.message(States.message_us)
@flags.chat_action("typing")
async def handle_message(msg: Message, state: FSMContext):
    print(msg.photo)
    print(msg)


@router.callback_query(F.data == "help")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.edit_text(text.help_text)
    await clbck.message.answer(text.exit_text, reply_markup=kb.exit_kb)


@router.callback_query(F.data == "send_photo")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(States.send_photo)
    await clbck.message.edit_text(text.send_photo_text)
    await clbck.message.answer(text.exit_text, reply_markup=kb.exit_kb)


@router.message(States.send_photo)
@flags.chat_action("typing")
async def handle_photo(msg: Message, state: FSMContext):
    file_id = msg.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, "text.jpg")
