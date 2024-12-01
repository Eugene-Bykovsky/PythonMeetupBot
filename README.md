# PythonMeetupBot #

Удобный телеграм бот на aiogram, оснащенный функционалом для качественного проведения организационных мироприятий.
## Installing

Перед использованием установите Python3. Дистрибутивы и инструкцию можно найти на [оффициальном сайте](https://www.python.org/downloads/)

Рекомендуется использовать пакеты из `requirements.txt`. 
Команда для установки: 
```
pip install -r requirements.txt`
```

## Telegram bot

Создаем бота через [BotFather](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram.html)

Получаем токен для использования [бота](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/#02:~:text=%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B%2C%20%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6%D0%B8%C2%BB.-,%D0%A1%D0%BE%D0%B7%D0%B4%D0%B0%D0%B5%D0%BC%20%D0%B1%D0%BE%D1%82%D0%B0,-%D0%A1%D0%BB%D0%B5%D0%B4%D1%83%D1%8E%D1%89%D0%B8%D0%B9%20%D1%88%D0%B0%D0%B3%20%E2%80%94%20%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5)


## Functional

Бот оснащен тремя сценариями пользования:

 ### `speaker.py`

Функции/кнопки:

- `/help` - Вызов справки

- `Программа мероприятия`

- `Список вопросов`

- `Задать вопрос`

### `user.py`

После запуска отобразит экран приветствия:

> Привет! Выберите действие:

Функции/кнопки:

- `/help` - Вызов справки

- `Программа мероприятия`

- `Задать вопрос`

- `Список вопросов`

### `event_organizers.py`


