from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from app.keyboards import speaker_keyboards

speaker = Router()


@speaker.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Выберите действие:", reply_markup=speaker_keyboards)


@speaker.message(F.text == "/help")
async def cmd_help(message: Message):
    await message.answer("справка")


@speaker.message(F.text == "Задать вопрос")
async def ask_question(message: Message):
    await message.answer("Пожалуйста, введите ваш вопрос:")


@speaker.message(F.text == "Программа мероприятия")
async def program(message: Message):
    await message.answer("Программа на сегодня:")


@speaker.message(F.text == "Список вопросов")
async def question_list(message: Message):
    await message.answer("Ваш список вопросов")