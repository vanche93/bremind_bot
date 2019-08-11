
from __future__ import print_function
from parser import import_dt, import_text
from bot import bot
from config import sdir
import subprocess
import re
#Функция отвечает на стартовое сообщение
@bot.message_handler(commands=['start', 'help',])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Привет, я бот котрый напомнит тебе что то сделать. \n Просто напиши мне что и когда тебе напомнить. \n Например "Выпить таблетки завтра днем" или "Забрать заказ 13 октября" \n Пока бот не умеет удалять созданые напоминания и часовой пояс MSK +3, но скоро я это все поправлю.')
#Функция обрабатывает текстовые сообщения
@bot.message_handler(content_types=['text'])
def in_text(message):
    #bot.send_message(message.chat.id, 'Я жив!')
    dt = import_dt(message.text)
    text = import_text(message.text)
    if dt == 'null' :
        bot.send_message(message.chat.id, 'Нужно указать время!')
    elif dt == 'old':
        bot.send_message(message.chat.id, 'Это уже в прошлом!')
    elif text == 'null':
        bot.send_message(message.chat.id, 'Нужно указать о чем вам напомнить!')
    else:
        add_task(message.chat.id,text, dt)
        answer = 'Я напомню тебе ' + text + ' ' + dt
        bot.send_message(message.chat.id, answer)
#Функция отправляет сообщения в чат пользователю
def send_message(id, text):
    bot.send_message(id, text)
#Функция создают задачу в AT и добавляет ее в бд
def add_task(id, text, date_time):
    cmd = 'echo "%s/send_message.py %s  \'%s\''' " | at %s' % (sdir, id, text, date_time)
    print(cmd)
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = out.communicate()
    print(stdout)

#Ожидать входящие сообщения
bot.polling()
