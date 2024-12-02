# PythonMeetupBot #

PythonMeetupBot is a Telegram bot designed to manage meetings, schedules, and notifications related to events and conferences.

## Installing

Before using, install Python 3. Distributions and instructions can be found on the [official website](https://www.python.org/downloads/)

It is recommended to use packages from `requirements.txt `. 
The command to install:
```
pip install -r requirements.txt`
```

## Telegram bot

1. Creating a bot via [BotFathe](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram.html)

2. Getting a token to use [bot](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/#02:~:text=%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B%2C%20%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6%D0%B8%C2%BB.-,%D0%A1%D0%BE%D0%B7%D0%B4%D0%B0%D0%B5%D0%BC%20%D0%B1%D0%BE%D1%82%D0%B0,-%D0%A1%D0%BB%D0%B5%D0%B4%D1%83%D1%8E%D1%89%D0%B8%D0%B9%20%D1%88%D0%B0%D0%B3%20%E2%80%94%20%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5)

3. We invite the bot via a token by specifying it in the environment variables as `TG_TOKEN`.

   `.env`
	```env
	TG_TOKEN = <ваш тг токен>
	```
4. Launch the bot `run.py `


## Functional

### **PythonMeetupBot**.
PythonMeetupBot using the aiogram library and asynchronous approach for high performance and efficient query processing.

Provides the following functions:

**Registration for the event**:
- _The ability to register as a listener via Telegram_.
- _Checking the registration status and the role of the user (listener or speaker)_.

**Information about the event**:
- _Getting detailed information about the event, including the name, description, start and end dates_.
- _Access to the schedule of reports with indication of time and speakers._
- _Ask a question to the speaker_

**Viewing a list of reports to choose from**:
- _Sending a question to the speaker with the option to specify a contact for feedback._
- _Working with questions for speakers_
- _Receiving a list of questions sent by the speaker based on his reports_._

**Convenient navigation buttons**:

_Interactive keyboards for quick interaction with the bot, including buttons for registration, role verification, receiving information and sending questions._

**Integration with the API**:

_User registration, role verification, schedule receipt, sending questions and receiving them are implemented through interaction with an external API._




 








 




