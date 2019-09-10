# -*- coding: utf-8 -*-
# BRemind created by Ivan Burashev in 2019 vanche93@yandex.ru

from datetime import datetime, time
from config import servertz
from rutimeparser import parse, get_clear_text
import pytz

def import_dt(text, timezone='Europe/Moscow'):  # Функция забирает дату и время из сообщения
    result = parse(text, tz=timezone, now=None, remove_junk=True,
                   allowed_results=(datetime, None),
                   default_time=time(12, 0), default_datetime=None)
    dt_text = result
    localtz = pytz.timezone(servertz)
    timezone = pytz.timezone(timezone)
    if result is None:
        return 'null', 'null'
    if datetime.now(tz=timezone) > result:
        return 'old', 'old'
    result = result.astimezone(tz=localtz)
    result = ('{:%H:%M %d.%m.%Y}'.format(result))
    dt_text = ('{:%H:%M %d.%m.%Y}'.format(dt_text))
    return result, dt_text

def import_text(text):  # Функция забирает текст из сообщения
    result = get_clear_text(text)
    if result == '':
        return 'null'
    return result
