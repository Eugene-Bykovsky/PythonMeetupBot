from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from app.keyboards import user_keyboards

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Выберите действие:", reply_markup=user_keyboards)


@user.message(F.text == "/help")
async def cmd_help(message: Message):
    await message.answer("справка")


@user.message(F.text == "Задать вопрос")
async def ask_question(message: Message):
    await message.answer("Пожалуйста, введите ваш вопрос:")


@user.message(F.text == "Программа мероприятия")
async def program(message: Message):
    await message.answer("Программа на сегодня:")


@user.message(F.text == "Список вопросов")
async def question_list(message: Message):
    await message.answer("Ваш список вопросов")
