from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_keyboards = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Задать вопрос")],
    [KeyboardButton(text="Программа мероприятия")]
], resize_keyboard=True, input_field_placeholder="Выберите пункт меню")


speaker_keyboards = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Задать вопрос")],
    [KeyboardButton(text="Программа мероприятия")],
    [KeyboardButton(text="Список вопросов")]
], resize_keyboard=True, input_field_placeholder="Выберите пункт меню")
