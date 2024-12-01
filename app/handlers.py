from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests

from app.keyboards import start_keyboard, listener_keyboard, speaker_keyboard


router = Router()


@router.message(F.text == "/start")
async def start_command(message: Message):
    await message.answer(
        "Добро пожаловать! Выберите действие:",
        reply_markup=start_keyboard
    )


@router.message(F.text == "/help")
async def start_command(message: Message):
    await message.answer("text")


@router.message(F.text == "Зарегистрироваться")
async def register_user(message: Message):
    params = {
        "event_id": 1,
        "telegram_id": message.from_user.id,
        "name": message.from_user.full_name
    }
    response = requests.post('http://51.250.44.171:8000/api/event-registrations/', json=params)
    if response.status_code:
        await message.answer("Вы успешно зарегистрированы как слушатель!", reply_markup=listener_keyboard)
    else:
        await message.answer(
            f"Ошибка при регистрации: {response.status_code}.\n{response.text}"
        )


@router.message(F.text == "Я уже зарегистрирован")
async def check_registration(message: Message):
    params = {
        "telegram_id": message.from_user.id
    }
    response = requests.get('http://51.250.44.171:8000/api/check-role/check-role/', params=params)
    if response.status_code:
        roles = response.json().get("roles", [])
        if "listener" in roles:
            await message.answer("Вы успешно вошли как слушатель!", reply_markup=listener_keyboard)
        elif "speaker" in roles:
            await message.answer("Вы вошли как докладчик!", reply_markup=speaker_keyboard)

