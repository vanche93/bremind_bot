import sqlite3


# Функция добавляет данные в таблицу 'tz'
def add_to_db_tz(id, username, timezone):
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    # Если таблицы не существует создать ее
    cursor.execute("""CREATE TABLE IF NOT EXISTS tz
                          (id text, username text, timezone text)
                       """)
    ins = """INSERT INTO tz VALUES ('%s', '%s', '%s')""" % (id, username, timezone)
    cursor.execute(ins)
    conn.commit()


# Чтение данных из таблицы 'tz'
def read_data_in_tz(chatid):
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tz WHERE chatid LIKE ?', [chatid])
    result = cursor.fetchall()
    print(result)


# Функция создает таблицу 'tasklist'
def greate_db_tasklist(chatid):
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    chatid = 'tasklist:' + str(chatid)
    # Если таблицы не существует создать ее
    cursor.execute("""CREATE TABLE IF NOT EXISTS '%s'
                          (number text, time text, text text, uid text)
                       """ % (chatid))


# Функция добавляет данные в таблицу 'tasklist'
def add_to_db_tasklist(chatid, number, time, text, uid):
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    chatid = 'tasklist:' + str(chatid)
    # Если таблицы не существует создать ее
    cursor.execute("""CREATE TABLE IF NOT EXISTS '%s'
                          (number text, time text, text text, uid text)
                       """ % (chatid))
    ins = """INSERT INTO '%s'  VALUES ('%s', '%s', '%s', '%s')""" % (chatid, number, time, text, uid)
    cursor.execute(ins)
    conn.commit()


# Чтение данных из таблицы 'tasklist'
def read_data_in_task(chatid):
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    chatid = 'tasklist:' + str(chatid)
    # Если таблицы не существует создать ее
    cursor.execute("""CREATE TABLE IF NOT EXISTS '%s'
                          (number text, time text, text text, uid text)
                       """ % (chatid))
    c = cursor.execute("""SELECT number,time,text FROM '%s'""" % (chatid))
    result = '*Номер задачи | Время | Задача* \n' + '\n'.join(['| '.join(map(str, x)) for x in c])
    print(result)
    return result


def delete_task(uid, chatid):
    chatid = 'tasklist:' + str(chatid)
    print(uid)
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    delete = """DELETE FROM '%s' WHERE uid = '%s' """ % (chatid, uid)
    cursor.execute(delete)
    conn.commit()
    print("Запись удалена" + uid)
