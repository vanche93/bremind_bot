import datetime
import re
import subprocess
import uuid

import telebot
from telebot import types

from config import sdir
from config import token
from db import add_to_db_tasklist, read_data_in_task, init_db, change_tz, get_user_tz
from parser import import_dt, import_text

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])  # Функция отвечает на команды 'start', 'help'
def start_message(message):
    tz_string = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
    bot.send_message(message.chat.id,
                     f"Привет, я бот котрый напомнит тебе что то сделать. \n"
                     f"Просто напиши мне что и когда тебе напомнить. \n"
                     f"Например \"Выпить таблетки завтра днем\" или \"Забрать заказ 13 октября\"\n"
                     f"Список напоминаний можно посмотреть с помощью команды /tasklist.\n"
                     f"Я работаю в часовом поясе:{tz_string} \n https://github.com/vanche93/bremind_bot/")


@bot.message_handler(commands=['tasklist'])  # Функция отвечает на комнаду tasklist
def start_message(message):
    text = read_data_in_task(message.chat.id)
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(commands=['timezone'])  # Функция отвечает на комнаду timezone
def timezone_message(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Изменить часовой пояс', callback_data='list_timezone'))
    if get_user_tz(message.chat.id) == 'none':
        bot.send_message(message.chat.id, 'Часовой пояс не установлен', reply_markup=keyboard)
    else:
        timezone = get_user_tz(message.chat.id)
        bot.send_message(message.chat.id, timezone, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])  # Функция обрабатывает текстовые сообщения
def in_text(message):
    timezone = get_user_tz(message.chat.id)
    if timezone == 'none':
        bot.send_message(message.chat.id, "Не установлен часовой пояс.\n"
                                          "Для изменения часового пояса введите команду /timezone")
    else:
        dt, dt_text = import_dt(message.text, get_user_tz(message.chat.id))
        text = import_text(message.text)
        if dt == 'null':
            bot.send_message(message.chat.id, 'Нужно указать время!')
        elif dt == 'old':
            bot.send_message(message.chat.id, 'Это уже в прошлом!')
        elif text == 'null':
            bot.send_message(message.chat.id, 'Нужно указать о чем вам напомнить!')
        else:
            add_task(message.chat.id, text, dt, dt_text)
            answer = 'Я напомню тебе ' + text + ' ' + dt_text
            bot.send_message(message.chat.id, answer)


def add_task(id, text, date_time, dt_text):  # Функция создают задачу в AT и добавляет ее в бд
    uid = uuid.uuid4()
    cmd = f"""echo "{sdir}/send_message.py {id}  \'{text}\' {uid} '' " | at {date_time}"""
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = str(out.communicate())
    number = re.search('job(.+?) at', stdout).group(1)
    add_to_db_tasklist(id, number, dt_text, text, uid)


@bot.callback_query_handler(func=lambda call: True)  # Реакция на кнопки
def callback(call):
    if call.data == 'list_timezone':
        list_timezone(call.message.chat.id)
    if call.data.startswith('set_timezone:'):
        timezone = call.data.split(':')[1]
        change_tz(call.message.chat.id, timezone)
        bot.answer_callback_query(call.id, show_alert=True, text='Часовой пояс установлен')
    if call.data == ' через 15 минут':
        later(call)
    if call.data == ' через час':
        later(call)
    if call.data == ' завтра':
        later(call)


def list_timezone(id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Europe/Moscow', callback_data='set_timezone:Europe/Moscow'))
    keyboard.add(types.InlineKeyboardButton(text='Europe/Kaliningrad', callback_data='set_timezone:Europe/Kaliningrad'),
                 types.InlineKeyboardButton(text='Europe/Samara', callback_data='set_timezone:Europe/Samara'))
    keyboard.add(types.InlineKeyboardButton(text='Asia/Yekaterinburg', callback_data='set_timezone:Asia/Yekaterinburg'),
                 types.InlineKeyboardButton(text='Asia/Omsk', callback_data='set_timezone:Asia/Omsk'))
    keyboard.add(types.InlineKeyboardButton(text='Asia/Krasnoyarsk', callback_data='set_timezone:Asia/Krasnoyarsk'),
                 types.InlineKeyboardButton(text='Asia/Irkutsk', callback_data='set_timezone:Asia/Irkutsk'))
    keyboard.add(types.InlineKeyboardButton(text='Asia/Yakutsk', callback_data='set_timezone:Asia/Yakutsk'),
                 types.InlineKeyboardButton(text='Asia/Vladivostok', callback_data='set_timezone:Asia/Vladivostok'))
    keyboard.add(types.InlineKeyboardButton(text='Asia/Magadan', callback_data='set_timezone:Asia/Magadan'),
                 types.InlineKeyboardButton(text='Asia/Kamchatka', callback_data='set_timezone:Asia/Kamchatka'))
    bot.send_message(id, 'Выберите часовой пояс', reply_markup=keyboard)


def later(call):
    call.message.text = call.message.text + call.data
    in_text(message=call.message)


if __name__ == '__main__':  # Ожидать входящие сообщения
    init_db()
    bot.polling()
