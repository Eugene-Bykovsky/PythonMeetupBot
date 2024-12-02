from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from event_programs import get_event_programs
import requests

from app.keyboards import start_keyboard, listener_keyboard, speaker_keyboard


router = Router()


class QuestionStates(StatesGroup):
    choosing_talk = State()
    writing_question = State()


@router.message(F.text == "/start")
async def start_command(message: Message):
    await message.answer(
        "Добро пожаловать! Выберите действие:",
        reply_markup=start_keyboard
    )


@router.message(F.text == "Help")
async def start_command(message: Message):
    await message.answer(
        """
        Навигация:\n
        "Зарегистрироваться" — Пройти регистрацию на мероприятие как слушатель.\n
        "Я уже зарегистрирован" — Проверить свою регистрацию и роль (слушатель или докладчик).
        """)


@router.message(F.text == "Зарегистрироваться")
async def register_user(message: Message):
    params = {
        "event_id": 10,
        "telegram_id": message.from_user.id,
        "name": message.from_user.full_name
    }
    response = requests.post('http://84.252.132.43:8000/api/event-registrations/', json=params)
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
    response = requests.get('http://84.252.132.43:8000/api/check-role/', params=params)
    if response.status_code:
        roles = response.json().get("roles", [])
        if "listener" in roles:
            await message.answer("Вы успешно вошли как слушатель!", reply_markup=listener_keyboard)
        elif "speaker" in roles:
            await message.answer("Вы вошли как докладчик!", reply_markup=speaker_keyboard)


@router.message(F.text == "Информация по мероприятию")
async def event_info(message: Message):
    event_programs = get_event_programs()
    if not event_programs:
        await message.answer("Нет доступных мероприятий.")
        return

    description = "Список программ:"
    keyboard_builder = InlineKeyboardBuilder()
    for event in event_programs:
        start_dt = datetime.strptime(event['start_date'], '%Y-%m-%dT%H:%M:%SZ')
        start_date = start_dt.strftime('%d.%m.%Y')  
        start_time = start_dt.strftime('%H:%M') 

        end_dt = datetime.strptime(event['end_date'], '%Y-%m-%dT%H:%M:%SZ')
        end_date = end_dt.strftime('%d.%m.%Y')      
        end_time = end_dt.strftime('%H:%M')      

        button_text = f"{event['title']}:\n{start_date} {start_time} - {end_date} {end_time}"
        button = InlineKeyboardButton(
            text=button_text,
            callback_data=f"event_id:{event['id']}"
        )
        keyboard_builder.add(button)
    keyboard = keyboard_builder.as_markup()
    await message.answer(description, reply_markup=keyboard)    


@router.message(F.text == "Задать вопрос")
async def ask_question_start(message: Message, state: FSMContext):
    response = requests.get('http://84.252.132.43:8000/api/talks/')
    if response.status_code:
        talks = response.json()
        if talks:
            keyboard_builder = InlineKeyboardBuilder()
            for talk in talks:
                button = InlineKeyboardButton(
                    text=f"{talk['title']} - {talk['speaker']}",
                    callback_data=f"talk_{talk['id']}"
                )
                keyboard_builder.add(button)
            keyboard = keyboard_builder.as_markup()
            await message.answer("Выберите доклад:", reply_markup=keyboard)
            await state.set_state(QuestionStates.choosing_talk)
        else:
            await message.answer("Список докладов недоступен.")
    else:
        await message.answer("Ошибка при получении списка докладов.")


@router.callback_query(QuestionStates.choosing_talk, F.data.startswith('talk_'))
async def choose_talk(callback: CallbackQuery, state: FSMContext):
    talk_id = int(callback.data.split('_')[1])
    await state.update_data(talk_id=talk_id)
    await callback.message.answer("Введите ваш вопрос:")
    await state.set_state(QuestionStates.writing_question)
    await callback.answer()


@router.message(QuestionStates.writing_question)
async def receive_question(message: Message, state: FSMContext):
    data = await state.get_data()
    talk_id = data.get("talk_id")
    user_id = message.from_user.id
    text = message.text

    question_data = {
        "text": text,
        "talk": talk_id,
        "telegram_id": user_id
    }
    response = requests.post('http://84.252.132.43:8000/api/questions/', json=question_data)
    if response.status_code:
        await message.answer("Ваш вопрос отправлен докладчику.")
    else:
        await message.answer(
            f"Ошибка при отправке вопроса: {response.status_code}.\n{response.text}"
        )
    await state.clear()


@router.message(F.text == "Получить вопросы")
async def get_questions(message: Message):
    speaker_telegram_id = message.from_user.id

    talks_response = requests.get('http://84.252.132.43:8000/api/talks/')
    talks_response.raise_for_status()
    talks = talks_response.json()

    speaker_talks = [talk for talk in talks if talk.get('speaker_telegram_id') == speaker_telegram_id]
    if not speaker_talks:
        await message.answer("У вас пока нет докладов.")
        return

    questions_response = requests.get('http://84.252.132.43:8000/api/questions/')
    questions_response.raise_for_status()
    questions = questions_response.json()

    speaker_talk_ids = [talk['id'] for talk in speaker_talks]

    speaker_questions = [q for q in questions if q['talk'] in speaker_talk_ids]

    if not speaker_questions:
        await message.answer("У вас пока нет вопросов.")
        return

    for question in speaker_questions:
        talk_id = question['talk']
        talk = next((t for t in speaker_talks if t['id'] == talk_id), None)
        talk_title = talk['title']

        user_telegram_id = question.get('telegram_id')

        question_text = (
            f"Доклад: {talk_title}\n"
            f"Вопрос: {question['text']}\n"
            f"Контакт пользователя: {user_telegram_id}"
        )
        await message.answer(question_text)
