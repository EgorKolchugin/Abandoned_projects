import sqlite3
import telebot
import random
from telebot import types

bot = telebot.TeleBot('6617610205:AAGXfXf8pqQQsws3hs6T9XYBBQ26PPYTz3M')

markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup4 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn1 = types.KeyboardButton(text='Просмотреть фото')
btn2 = types.KeyboardButton(text='Удалить фото')
btn3 = types.KeyboardButton(text='Вернуться')
btn4 = types.KeyboardButton(text='Добавить фото')
markup1.add(btn1)
markup2.add(btn2, btn3)
markup3.add(btn3, btn4)
markup4.add(btn1, btn2, btn3)
@bot.message_handler(commands=['start'])
def start(message):
    global multi
    first_number = random.randrange(1, 20)
    second_number = random.randrange(1, 20)
    multi = first_number + second_number
    msg = bot.send_message(message.chat.id, text=f'Пройдите капчу\n<b>{first_number} + {second_number}</b>\nРезультат напишите ниже:', parse_mode='html')
    bot.register_next_step_handler(msg, callback=captcha)

@bot.callback_query_handler(func=lambda call: call.data == 'captcha')
def captcha(call):
    try:
        global passing
        if int(call.text) == multi:
            passing = 1
            db = sqlite3.connect('srver.db')
            sql = db.cursor()
            sql.execute("""CREATE TABLE IF NOT EXISTS tg(
                        user TEXT,
                        secret BLOB
                        )""")
            db.commit()
            sql.execute(f"SELECT user FROM tg WHERE user = '{call.from_user.id}'")
            if sql.fetchone() == None:
                sql.execute(f"INSERT INTO tg VALUES (?, ?)",(call.from_user.id, 0))
                db.commit()
                bot.send_message(call.from_user.id, text=f'Добро пожаловать, {call.from_user.first_name}!', reply_markup=markup1)
                db.close()
            else:
                bot.send_message(call.from_user.id, text=f'Добро пожаловать, {call.from_user.first_name}!', reply_markup=markup1)
                db.close()
        else:
            start(call)
    except:
        start(call)

@bot.message_handler(content_types='text')
def secret(message):
    # try:
        if passing == 1:
            if message.text == 'Просмотреть фото':
                db = sqlite3.connect('srver.db')
                sql = db.cursor()
                sql.execute(f"SELECT secret FROM tg WHERE user = '{message.from_user.id}'")
                img = sql.fetchone()
                if sql.fetchone() != None:
                    bot.send_message(message.chat.id, text=(f'{img}'), reply_markup=markup2)
                    db.close()
                else:
                    bot.send_message(message.chat.id, text='Фото не обнаружено', reply_markup=markup3)
                    db.close()
            elif message.text == 'Удалить фото':
                db = sqlite3.connect('srver.db')
                sql = db.cursor()
                sql.execute(f"UPDATE tg SET secret = 0 WHERE user ='{message.from_user.id}' ")
                db.commit()
                bot.send_message(message.from_user.id, text='Фото удалено')
                db.close()
            elif message.text == 'Вернуться':
                captcha(message)
            elif message.text == 'Добавить фото':
                msg = bot.send_message(message.chat.id, text='Отправьте фото')
                bot.register_next_step_handler(msg, callback=image)
            else:
                captcha(message)
        else:
            captcha(message)
    # except:
        # pass
        # start(message)

@bot.callback_query_handler(func=lambda call:call.data == 'image')
def image(call):
    if call.content_type == 'photo':
        db = sqlite3.connect('srver.db')
        sql = db.cursor()
        file_info = bot.get_file(call.photo[-1].file_id).file_path
        downloaded_file = bot.download_file(file_info)
        src = file_info
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            sql.execute(f"UPDATE tg SET secret = {open(file_info, 'rb')} WHERE user ='{call.from_user.id}'")
            db.commit()
            db.close()
            bot.send_message(call.from_user.id, text='Фото обновлено', reply_markup=markup4)
    else:
        bot.send_message(call.from_user.id, text='Отправлено не фото')
        captcha(call)
bot.infinity_polling()


# db = sqlite3.connect('srver.db')

# sql = db.cursor()

# sql.execute("""CREATE TABLE IF NOT EXISTS site(
#             login TEXT,
#             password TEXT
# )""")
# db.commit()
# def reg():
#     reg_u = input('Введите логин\n')
#     sql.execute(f"SELECT login FROM site WHERE login ='{reg_u}'")
#     if sql.fetchone() is None:
#         a = input('Указан неверный логин\nЧтобы зарегистрироваться введите: reg\n')
#         if a == 'reg':
#             reg_l = input('Введите логин\n')
#             reg_p = input('Введите пароль\n')
#             sql.execute(f"INSERT INTO site VALUES (?, ?)",(reg_l, reg_p))
#             print('Регистрация завершена!')
#             db.commit()
#         else:
#             reg()
#     else:
#         p_p = input('Введите пароль\n')
#         sql.execute(f"SELECT password FROM site WHERE login = '{reg_u}'")
#         if sql.fetchone() != p_p:
#             print('Неверный пароль')
#             reg()
#         else:
#             print('Добро пожаловать!')
# reg()