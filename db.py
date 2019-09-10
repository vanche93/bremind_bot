import sqlite3

def init_db():
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    # Если таблицы не существует создать ее
    cursor.execute("""CREATE TABLE IF NOT EXISTS 'users'
                              (id text, tz text)
                           """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS 'tasklist'
                                  (id text, number text, time text, text text, uid text)
                               """)
    conn.commit()

def add_user(id, tz='EUROPE/MOSCOW'): # Добавление нового пользователя
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    ins = f"""INSERT INTO 'users'  VALUES ('{id}', '{tz}')"""
    cursor.execute(ins)
    conn.commit()

def add_to_db_tasklist(chatid, number, time, text, uid):  # Функция добавляет данные в таблицу 'tasklist'
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    ins = f"""INSERT INTO 'tasklist'  VALUES ('{chatid}', '{number}', '{time}', '{text}', '{uid}')"""
    cursor.execute(ins)
    conn.commit()


def read_data_in_task(chatid):  # Чтение данных из таблицы 'tasklist'
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    c = cursor.execute(f"""SELECT number,time,text FROM 'tasklist' WHERE id={chatid}""")
    result = '*Номер задачи | Время | Задача* \n' + '\n'.join(['| '.join(map(str, x)) for x in c])
    print(result)
    return result


def delete_task(uid):  # Удаление данных из таблицы 'tasklist'
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    delete = f"""DELETE FROM 'tasklist' WHERE uid = '{uid}' """
    cursor.execute(delete)
    conn.commit()
