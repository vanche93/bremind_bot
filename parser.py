# -*- coding: utf-8 -*-
# BRemind created by Ivan Burashev in 2019 vanche93@yandex.ru

from datetime import datetime, time

from rutimeparser import parse, get_clear_text


def import_dt(text):  # Функция забирает дату и время из сообщения
    result = parse(text, now=None, remove_junk=True,
                   allowed_results=(datetime, None),
                   default_time=time(12, 0), default_datetime=None)
    if result is None:
        return 'null'
    if datetime.now() > result:
        return 'old'
    result = ('{:%H:%M %d.%m.%Y}'.format(result))
    return result


def import_text(text):  # Функция забирает текст из сообщения
    result = get_clear_text(text)
    if result == '':
        return 'null'
    return result
