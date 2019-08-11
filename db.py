import sqlite3

conn = sqlite3.connect("db.db")
cursor = conn.cursor()

#Функция добавляет данные в таблицу 'tz'
def add_to_db_tz(id, username, timezone):
    #Если таблицы не существует создать ее
    cursor.execute("""CREATE TABLE IF NOT EXISTS tz
                          (id text, username text, timezone text)
                       """)
    ins = """INSERT INTO tz VALUES ('%s', '%s', '%s')""" % (id, username, timezone)
    cursor.execute(ins)
    conn.commit()
#Чтение данных из таблицы 'tz'
def read_data_in_tz(chatid):
    cursor.execute('SELECT * FROM tz WHERE chatid LIKE ?', [chatid])
    result =  cursor.fetchall()
    print(result)

#Функция добавляет данные в таблицу 'tasklist'
def add_to_db_tasklist(chatid, number, time, text):
    #Если таблицы не существует создать ее
    cursor.execute("""CREATE TABLE IF NOT EXISTS '%s'
                          (number text, time text, text text)
                       """ % (chatid))
    chatid = 'tasklist:' + str(chatid)
    ins = """INSERT INTO '%s'  VALUES ('%s', '%s', '%s')""" % (chatid, number, time, text)
    cursor.execute(ins)
    conn.commit()
#Чтение данных из таблицы 'tasklist'
def read_data_in_task(chatid):
    chatid = 'tasklist:' + str(chatid)
    cursor.execute("""SELECT * FROM '%s'""" % (chatid))
    result =  cursor.fetchall()
    print(result)


#add_to_db('ид3','user3','Amsterdam3')
#read_data_in_tz('ид')
#add_to_db_tasklist('777777', '2', '16:30', 'test')
#read_data_in_task('777777')

#print(cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='tasklist:777777'"""))