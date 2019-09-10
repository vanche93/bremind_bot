#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys

from telebot import types

from db import delete_task
from main import bot

logging.basicConfig(filename="send_message.log", level=logging.INFO)


def send_message(id, text):  # Функция отправляет сообщения в чат пользователю
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Напомнить через 15 минут', callback_data=' через 15 минут'))
    keyboard.add(types.InlineKeyboardButton(text='Напомнить через час', callback_data=' через час'))
    keyboard.add(types.InlineKeyboardButton(text='Напомнить завтра', callback_data=' завтра'))
    bot.send_message(id, text, reply_markup=keyboard)
    logging.info(id)
    logging.info(text)


if __name__ == "__main__":
    send_message(sys.argv[1], sys.argv[2])
    delete_task(uid=sys.argv[3])
