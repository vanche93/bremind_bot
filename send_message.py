#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BRemind v0.1 created by Ivan Burashev in 2019 vanche93@yandex.ru

# Скрипт принимает два аргумента ид и сообщение
# Пример использования:
# ./send_message.py 267187987 'Сообщение из консоли'

import logging
import sys
from bot import bot
from telebot import types
from main import add_task, in_text
from db import delete_task

logging.basicConfig(filename="send_message.log", level=logging.INFO)


# Функция отправляет сообщения в чат пользователю
def send_message(id, text, uid):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=' через 15 минут') for name in
                   ['Напомнить через 15 минут']])
    keyboard.add(
        *[types.InlineKeyboardButton(text=name, callback_data=' через час') for name in ['Напомнить через час']])
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=' завтра') for name in ['Напомнить завтра']])
    bot.send_message(id, text, reply_markup=keyboard)
    logging.info(id)
    logging.info(text)


if __name__ == "__main__":
    send_message(sys.argv[1], sys.argv[2], sys.argv[3])
    delete_task(uid=sys.argv[3], chatid=sys.argv[1])
