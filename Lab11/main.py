from datetime import datetime, timedelta
import requests
import shutil

import psycopg2
import telebot
from telebot import types

conn = psycopg2.connect(database="postgres", user="postgres", password="12345", host="localhost",
                        port="5432")
cursor = conn.cursor()

bot = telebot.TeleBot("6578758432:AAEMsfm8pmxByxFKUp11oBGz4ecfWXSQGVk")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 "Привет! Я бот с расписанием учебной группы. Доступные команды:\n/week - узнать текущую неделю\n/kstu - получить ссылку на КНИТУ\n/help - показать это сообщение снова")
    send_week_buttons(message.chat.id)


@bot.message_handler(commands=['week'])
def current_week(message):
    today = datetime.now()
    week_number = today.isocalendar()[1]
    parity = "нижняя" if week_number % 2 == 0 else "верхняя"
    bot.reply_to(message, f"Сейчас {parity} неделя.")


@bot.message_handler(commands=['cat'])
def current_week(message):
    r = requests.get("https://cataas.com/cat", stream=True)
    if r.status_code == 200:
        with open("cat.jpg", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    bot.send_photo(message.chat.id, photo=open('cat.jpg', 'rb'))


@bot.message_handler(content_types=["text"])
def want_handler(message):
    if message.text.lower() == "хочу":
        bot.send_message(message.chat.id, "Тогда тебе сюда - https://www.kstu.ru")
    else:
        bot.send_message(message.chat.id, "Извините, я Вас не понял")


@bot.message_handler(commands=['kstu'])
def kstu_link(message):
    bot.reply_to(message, "Ссылка на КНИТУ: https://www.kstu.ru")


@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.reply_to(message, "Извините, я Вас не понял.")


def get_schedule(day):
    cursor.execute(
        "SELECT timetable.subject, room_number, start_time, full_name FROM timetable INNER JOIN subject ON timetable.subject = subject.name INNER JOIN teacher ON subject.name = teacher.subject WHERE day = %s",
        (day,))
    schedule = cursor.fetchall()
    return schedule


def format_schedule(schedule):
    formatted_schedule = ""
    for entry in schedule:
        subject, room_number, start_time, teacher = entry
        formatted_schedule += f"{subject} {room_number} {start_time.strftime('%H:%M')} {teacher}\n"
    return formatted_schedule.strip()


@bot.callback_query_handler(func=lambda call: call.data in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'])
def callback_handler(call):
    day_mapping = {'monday': 'Понедельник', 'tuesday': 'Вторник', 'wednesday': 'Среда', 'thursday': 'Четверг',
                   'friday': 'Пятница'}
    day = day_mapping[call.data]
    schedule = get_schedule(day)
    if schedule:
        formatted_schedule = format_schedule(schedule)
        bot.send_message(call.message.chat.id, f"{day.capitalize()}\n--------------\n{formatted_schedule}")
    else:
        bot.send_message(call.message.chat.id, "Расписание на этот день отсутствует.")


@bot.callback_query_handler(func=lambda call: call.data == 'current_week')
def current_week_schedule(call):
    send_week_buttons(call.message.chat.id)
    today = datetime.now()
    schedule = get_week_schedule(today)
    formatted_schedule = format_week_schedule(schedule)
    bot.send_message(call.message.chat.id, f"Расписание на эту неделю:\n{formatted_schedule}")


@bot.callback_query_handler(func=lambda call: call.data == 'next_week')
def next_week_schedule(call):
    next_week = datetime.now() + timedelta(days=7)
    send_week_buttons(call.message.chat.id)
    schedule = get_week_schedule(next_week)
    formatted_schedule = format_week_schedule(schedule)
    bot.send_message(call.message.chat.id, f"Расписание на следующую неделю:\n{formatted_schedule}")


def format_week_schedule(week_schedule):
    day_mapping = {'monday': 'Понедельник', 'tuesday': 'Вторник', 'wednesday': 'Среда', 'thursday': 'Четверг',
                   'friday': 'Пятница', 'saturday': 'Суббота', 'sunday': 'Воскресенье'}
    formatted_schedule = ""
    for day, schedule in week_schedule.items():
        formatted_schedule += f"{day_mapping[day.lower()].capitalize()}\n--------------\n"
        formatted_schedule += format_schedule(schedule) + "\n\n"
    return formatted_schedule.strip()


def get_week_schedule(start_date):
    day_mapping = {'monday': 'Понедельник', 'tuesday': 'Вторник', 'wednesday': 'Среда', 'thursday': 'Четверг',
                   'friday': 'Пятница', 'saturday': 'Суббота', 'sunday': 'Воскресенье'}
    week_schedule = {}
    for i in range(7):
        day = start_date + timedelta(days=i)
        day_name = day.strftime("%A")
        schedule = get_schedule(day_mapping[day_name.lower()])
        week_schedule[day_name] = schedule
    return week_schedule


def send_week_buttons(chat_id):
    markup = types.InlineKeyboardMarkup()
    day_mapping = {'monday': 'Понедельник', 'tuesday': 'Вторник', 'wednesday': 'Среда', 'thursday': 'Четверг',
                   'friday': 'Пятница'}
    for callback_day in day_mapping:
        markup.add(types.InlineKeyboardButton(text=day_mapping[callback_day], callback_data=callback_day))
    markup.add(types.InlineKeyboardButton(text='Расписание на текущую неделю', callback_data='current_week'))
    markup.add(types.InlineKeyboardButton(text='Расписание на следующую неделю', callback_data='next_week'))
    bot.send_message(chat_id, "Выберите день недели или неделю:", reply_markup=markup)


bot.polling()
