from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm import context
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.chat_action import ChatActionMiddleware

BOT_TOKEN = '6919330886:AAEVpiswCzxhUejDpqk6CPkIhh_YdiyXmC8'
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
