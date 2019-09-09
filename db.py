import sqlite3


def add_to_db_tasklist(chatid, number, time, text, uid):  # Функция добавляет данные в таблицу 'tasklist'
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


def read_data_in_task(chatid):  # Чтение данных из таблицы 'tasklist'
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


def delete_task(uid, chatid):  # Удаление данных из таблицы 'tasklist'
    chatid = 'tasklist:' + str(chatid)
    print(uid)
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    delete = """DELETE FROM '%s' WHERE uid = '%s' """ % (chatid, uid)
    cursor.execute(delete)
    conn.commit()
    print("Запись удалена" + uid)
