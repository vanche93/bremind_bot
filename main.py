import re
import subprocess
import uuid
import datetime
import telebot

from config import sdir
from config import token
from db import add_to_db_tasklist, read_data_in_task,init_db
from parser import import_dt, import_text

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])  # Функция отвечает на команды 'start', 'help'
def start_message(message):
    tz_string = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
    bot.send_message(message.chat.id,
                     f'Привет, я бот котрый напомнит тебе что то сделать. \n Просто напиши мне что и когда тебе напомнить. \n Например "Выпить таблетки завтра днем" или "Забрать заказ 13 октября"\n Список напоминаний можно посмотреть с помощью команды /tasklist.\n Я работаю в часовом поясе:{tz_string} \n https://github.com/vanche93/bremind_bot/')


@bot.message_handler(commands=['tasklist'])  # Функция отвечает на комнаду tasklist
def start_message(message):
    text = read_data_in_task(message.chat.id)
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(content_types=['text'])  # Функция обрабатывает текстовые сообщения
def in_text(message):
    dt = import_dt(message.text)
    text = import_text(message.text)
    if dt == 'null':
        bot.send_message(message.chat.id, 'Нужно указать время!')
    elif dt == 'old':
        bot.send_message(message.chat.id, 'Это уже в прошлом!')
    elif text == 'null':
        bot.send_message(message.chat.id, 'Нужно указать о чем вам напомнить!')
    else:
        add_task(message.chat.id, text, dt)
        answer = 'Я напомню тебе ' + text + ' ' + dt
        bot.send_message(message.chat.id, answer)


def add_task(id, text, date_time):  # Функция создают задачу в AT и добавляет ее в бд
    uid = uuid.uuid4()
    cmd = f"""echo "{sdir}/send_message.py {id}  \'{text}\' {uid} '' " | at {date_time}"""
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = str(out.communicate())
    number = re.search('job(.+?) at', stdout).group(1)
    add_to_db_tasklist(id, number, date_time, text, uid)


@bot.callback_query_handler(func=lambda call: True) # Реакция на кнопки отложить
def later(call):
    call.message.text = call.message.text + call.data
    in_text(message=call.message)


if __name__ == '__main__':  # Ожидать входящие сообщения
    init_db()
    bot.polling()
