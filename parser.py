#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
# BRemind v0.1 created by Ivan Burashev in 2019 vanche93@yandex.ru


from rutimeparser import parse, get_clear_text, get_last_clear_text
from datetime import datetime, date, time


#Функция забирает дату и время из сообщения
def import_dt(text):
    result = parse(text, now=None, remove_junk=True,
          allowed_results=(datetime, None),
          default_time=time(12, 0), default_datetime=None)
    if result is None:
        return 'null'
    if datetime.now() > result:
        return 'old'
    result = ('{:%H:%M %d.%m.%Y}'.format(result))
    return result
#Функция забирает текст из сообщения
def import_text(text):
    result = get_last_clear_text(text)
    if result == '':
        return 'null'
    return result