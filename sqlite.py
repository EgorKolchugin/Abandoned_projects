import sqlite3
from random import randint

db = sqlite3.connect('server.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
            login TEXT,
            password TEXT,
            cash BIGINT
)""")
db.commit()
def reg():
    user_login = input('Login: ')
    user_password = input('Password: ')

    sql.execute(f"SELECT login FROM users WHERE login ='{user_login}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES (?, ?, ?)", (user_login, user_password, 0))
        db.commit()
        print('Зарегестрировано!')
    else:
        print('Такая запись уже есть!')
        
        for value in sql.execute("SELECT * FROM users"):
            print(value[0])
def delete_db():
    sql.execute(f'DELETE FROM users WHERE login = "{user_login}"')
    db.commit()
    print('Запись удалена!')

def casino():
    global user_login
    user_login = input('Login: ')
    number = randint(1, 2)

    for i in sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'"):
        balance = i[0]

    sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
    if sql.fetchone() is None:
        print('Такого логина не существует. Зарегистрируйтесь')
        reg()
    else:
        if number == 1:
            print('Вы выйграли')
            sql.execute(f'UPDATE users SET cash = {1000 + balance} WHERE login ="{user_login}"')
            db.commit()
        else:
            print('Вы проиграли')
            sql.execute(f'UPDATE users SET cash = {balance - 1000} WHERE login ="{user_login}"')
            db.commit()
        if balance < 0:
            print('За вами должок')
        else:
            pass

def enter():
    # for i in sql.execute('SELECT login, cash FROM users'):
    #     print(i)
    sql.execute('SELECT login, cash FROM users')
    row = sql.fetchall()
    print(row)
def main():
    casino()
    enter()


main()