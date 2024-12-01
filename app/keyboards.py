from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Help")],
        [KeyboardButton(text="Зарегистрироваться")],
        [KeyboardButton(text="Я уже зарегистрирован")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню"
)


listener_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Информация по мероприятию")],
        [KeyboardButton(text="Задать вопрос")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)


speaker_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Информация по мероприятию")],
        [KeyboardButton(text="Получить вопросы")],
        [KeyboardButton(text="Задать вопрос")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)
