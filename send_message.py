#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys

from telebot import types

from db import delete_task
from main import bot

logging.basicConfig(filename="send_message.log", level=logging.INFO)


def send_message(id, text, uid):  # Функция отправляет сообщения в чат пользователю
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
    delete_task(uid=sys.argv[3])
