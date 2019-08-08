#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BRemind v0.1 created by Ivan Burashev in 2019 vanche93@yandex.ru

#Скрипт принимает два аргумента ид и сообщение
#Пример использования:
#./send_message.py 267187987 'Сообщение из консоли'

import logging
import sys
from bot import bot

logging.basicConfig(filename="send_message.log", level=logging.INFO)

#Функция отправляет сообщения в чат пользователю
def send_message(id, text):
    bot.send_message(id, text)
    logging.info(id)
    logging.info(text)

if __name__ == "__main__":
    send_message(sys.argv[1],sys.argv[2])