import sqlite3


def add_to_db_tasklist(chatid, number, time, text, uid):  # Функция добавляет данные в таблицу 'tasklist'
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    chatid = 'tasklist:' + str(chatid)
    # Если таблицы не существует создать ее
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS '{chatid}'
                          (number text, time text, text text, uid text)
                       """)
    ins = f"""INSERT INTO '{chatid}'  VALUES ('{number}', '{time}', '{text}', '{uid}')"""
    cursor.execute(ins)
    conn.commit()


def read_data_in_task(chatid):  # Чтение данных из таблицы 'tasklist'
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    chatid = 'tasklist:' + str(chatid)
    # Если таблицы не существует создать ее
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS '{chatid}'
                          (number text, time text, text text, uid text)
                       """)
    c = cursor.execute(f"""SELECT number,time,text FROM '{chatid}'""")
    result = '*Номер задачи | Время | Задача* \n' + '\n'.join(['| '.join(map(str, x)) for x in c])
    return result


def delete_task(uid, chatid):  # Удаление данных из таблицы 'tasklist'
    chatid = 'tasklist:' + str(chatid)
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    delete = f"""DELETE FROM '{chatid}' WHERE uid = '{uid}' """
    cursor.execute(delete)
    conn.commit()
