from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests
from app.сorrect_time import format_datetime_to_msk

from app.keyboards import start_keyboard, listener_keyboard, speaker_keyboard


router = Router()


class QuestionStates(StatesGroup):
    choosing_talk = State()
    writing_question = State()


@router.message(F.text == "/start")
async def start_command(message: Message):
    user_name = message.from_user.first_name
    await message.answer(
        f"Привет, {user_name}! 🙋‍♂️\n"
        "Я ваш помощник по мероприятию: помогу зарегистрироваться, узнать информацию о мероприятии и задать вопросы спикерам.\n\n"
        "Выберите 'Зарегистрироваться' если вы тут впервые, либо войдите если уже регистрировались🚀",
        reply_markup=start_keyboard
    )


@router.message(F.text == "/help")
async def help_command(message: Message):
    await message.answer(
        "Навигация:\n\n"
        "1. \"Зарегистрироваться\" — Пройти регистрацию на мероприятие как слушатель.\n"
        "2. \"Я уже зарегистрирован\" — Проверить свою регистрацию и роль (слушатель или докладчик).\n"
        "3. \"Информация по мероприятию\" — Информация о докладах и дате/времени начала мероприятия.\n"
        "4. \"Задать вопрос\" — Задать вопрос по интересующему вас докладу."
    )


@router.message(F.text == "Зарегистрироваться")
async def register_user(message: Message):
    params = {
        "event_id": 10,
        "telegram_id": message.from_user.id,
        "name": message.from_user.full_name
    }
    response = requests.post('http://158.160.134.159:8000/api/event-registrations/', json=params)
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
    response = requests.get('http://158.160.134.159:8000/api/check-role/', params=params)
    if response.status_code:
        roles = response.json().get("roles", [])
        if "listener" in roles:
            await message.answer("Вы успешно вошли как слушатель!", reply_markup=listener_keyboard)
        elif "speaker" in roles:
            await message.answer("Вы вошли как докладчик!", reply_markup=speaker_keyboard)


@router.message(F.text == "Информация по мероприятию")
async def event_program_info(message: Message):
    event_response = requests.get('http://158.160.134.159:8000/api/event-programs/')
    event_response.raise_for_status()
    events = event_response.json()

    if not events:
        await message.answer("Информация о мероприятии отсутствует.")
        return

    event = events[0]
    event_info = (
        f"Мероприятие: {event['title']}\n"
        f"Описание: {event['description']}\n"
        f"Дата начала: {format_datetime_to_msk(event['start_date'])}\n"
        f"Дата окончания: {format_datetime_to_msk(event['end_date'])}\n\n"
    )

    talks_response = requests.get('http://158.160.134.159:8000/api/talks/')
    talks_response.raise_for_status()
    talks = talks_response.json()

    if talks:
        talks_info = "Доклады:\n"
        for talk in talks:
            talks_info += (
                f"- {talk['title']} (Спикер: {talk['speaker']})\n"
                f"  Время: {format_datetime_to_msk(talk['start_time'])} — {format_datetime_to_msk(talk['end_time'])}\n\n"
            )
    else:
        talks_info = "Доклады: Нет доступных докладов.\n"
    await message.answer(event_info + talks_info)


@router.message(F.text == "Задать вопрос")
async def ask_question_start(message: Message, state: FSMContext):
    response = requests.get('http://158.160.134.159:8000/api/talks/')
    talks = response.json()
    if talks:
        keyboard_builder = InlineKeyboardBuilder()
        for talk in talks:
            button = InlineKeyboardButton(
                text=f"{talk['title']}",
                callback_data=f"talk_{talk['id']}"
            )
            keyboard_builder.row(button)

        keyboard = keyboard_builder.as_markup()
        await message.answer("Выберите доклад:", reply_markup=keyboard)
        await state.set_state(QuestionStates.choosing_talk)
    else:
        await message.answer("Список докладов недоступен.")


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

    telegram_username = message.from_user.username

    if telegram_username:
        text += f"\nКонтакт для обратной связи: @{telegram_username}"
    else:
        text += "\nПользователь не оставил контакта для обратной связи."

    question_data = {
        "text": text,
        "talk": talk_id,
        "telegram_id": user_id
    }
    response = requests.post('http://158.160.134.159:8000/api/questions/', json=question_data)
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

    talks_response = requests.get('http://158.160.134.159:8000/api/talks/')
    talks_response.raise_for_status()
    talks = talks_response.json()

    speaker_talks = [talk for talk in talks if talk.get('speaker_telegram_id') == speaker_telegram_id]
    if not speaker_talks:
        await message.answer("У вас пока нет докладов.")
        return

    questions_response = requests.get('http://158.160.134.159:8000/api/questions/')
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

        question_text = (
            f"Доклад: {talk_title}\n"
            f"Вопрос: {question['text']}"
        )
        await message.answer(question_text)
