import socket
import random
import sqlite3
import random

def registration(data):
    l = []
    for i in data:
        l.append(i)
    email = l[0]
    login = l[1]
    password = l[2]
    id = random.randint(1000, 9999)
    print(email, login, password)
    db = sqlite3.connect('messager.db')
    sql = db.cursor()
    # sql.execute("""CREATE TABLE IF NOT EXISTS users(
    #             email TEXT,
    #             id TEXT,
    #             login TEXT,
    #             password TEXT,
    #             friends TEXT
    # )""")
    sql.execute(f'SELECT email FROM users WHERE email = "{email}"')
    if sql.fetchone() != None:
        msg_user_is_here = 'Данный пользователь существует!'
        conn.send(msg_user_is_here.encode('utf-8'))
        db.close()
    else:
        sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?)",(email, id, login, password, None))
        db.commit()
        login = login
        msg = f'Регистрация завершена.\nДобро пожаловать, {login}!'
        conn.send(msg.encode('utf-8'))
        db.close()
def login_(email, password, login):
    db = sqlite3.connect('messager.db')
    sql = db.cursor()
    sql.execute(f"SELECT password FROM users WHERE email = '{email}'")
    if sql.fetchone() == password:
        msg = f'Добро пожаловать, {login}!'
        conn.send(msg.encode('utf-8'))
        # Остальной код
    else:
        conn.send('Почта или пароль неверны!')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', 56943))
while True:
    sock.listen(144)
    conn, addr = sock.accept()
    print ('connected:', addr)
    data = conn.recv(1024)
    if not data:
        break
    else:
        data = data.decode('utf-8')
        print(data)
        d = data.split()
        registration(d)
        print(f'Подключение {addr} завершено')
sock.close()