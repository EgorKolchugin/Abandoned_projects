import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

bot = telebot.TeleBot('...') # Токен бота

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Ozon')
    btn2 = types.KeyboardButton(text='Wildberries')
    markup.add(btn1,btn2)
    bot.send_message(message.chat.id, text='Добро пожаловать!\nВыберите сайт для поиска товара', reply_markup=markup)

@bot.message_handler(content_types='text')
def owb(message):
    if message.text == 'Ozon':
        msg = bot.send_message(message.chat.id, text='Введите название товара') 
        bot.register_next_step_handler(msg, callback=ozon)
    elif message.text == 'Wildberries':
        msg = bot.send_message(message.chat.id, text='Введите название товара') 
        bot.register_next_step_handler(msg, callback=Wildberries)
    else: 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Ozon')
        btn2 = types.KeyboardButton('Wildberries')
        bot.send_message(message.chat.id, text='Выберите сайт для поиска товара', reply_markup=markup)
        markup.add(btn1,btn2)

@bot.callback_query_handler(func=lambda call: call.data == 'Wildberries')
def Wildberries(call):
    bot.send_message(call.chat.id, text='Пожалуйста подождите')
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument('--headless')
    # option.add_argument('user-agent=Mozilla/5.0 (Linux; Android 7.1; Mi A1 Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko)')
    driver = webdriver.Chrome(options=option)
    driver.get(f'https://www.wildberries.ru/catalog/0/search.aspx?search={call.text}')
    time.sleep(3)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(5)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(5)
    html = driver.page_source
    bs = BeautifulSoup(html, 'lxml')
    cards = bs.find_all(class_='product-card product-card--hoverable j-card-item')
    if cards == []:
        bot.send_message(call.chat.id, text='Товар не найден')
        owb(call)
    else:
        for card in cards:
            try:
                # img_url = card.find(class_='product-card__img-wrap img-plug j-thumbnail-wrap').img.get('src')
                url = card.find(class_='product-card__link j-card-link j-open-full-product-card').get('href')
                name = card.find(class_='product-card__brand-wrap').text
                price = card.find(class_='price__lower-price').text
                # ('span', {'class': 'price__wrap'}).text
                bot.send_message(call.chat.id, text=f'<b>Наименование:</b> {name} \n<b>Цена:</b> {price}\n<a href=\"{url}\"><b>Ссылка</b></a>',parse_mode='html')
            except:
                print('ERROR')
                continue
        owb(call)
    

    driver.close()
    driver.quit()

@bot.callback_query_handler(func=lambda call: call.data == 'ozon')
def ozon(call):
    bot.send_message(call.chat.id, text='Пожалуйста подождите')
    option = webdriver.ChromeOptions()
    # option.add_argument('--disable-blink-features=AutomationControlled')
    # option.add_argument('--headless')
    # option.add_argument('user-agent=Mozilla/5.0 (Linux; Android 7.1; Mi A1 Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko)')
    driver = webdriver.Chrome(options=option)
    driver.get(f'https://www.ozon.ru/search/?text={call.text}&from_global=true')
    time.sleep(3)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(3)
    html = driver.page_source
    bs = BeautifulSoup(html, 'lxml')
    cards = bs.find_all(class_='j9i ik')
    print(html)
    if cards == []:
        cards = bs.find_all(class_='ij8 j8i')
        if cards == []:
                cards = bs.find_all(class_='ij8 ji8')
                if cards == []:
                    bot.send_message(call.chat.id, text='Товар не найден')
                    owb(call)
                else:
                    for card in cards:
                        try:
                            get_image = card.find(class_='hy7').img.get('src')
                            img_url = get_image
                            get_url = card.find(class_='tile-hover-target h2y hy3').get('href')
                            url = f'https://ozon.ru{get_url}'
                            name = card.find(class_='xd3 d4x x4d h2y hy3').text
                            price = card.find('span', {'class': 'c3-a1 tsHeadline500Medium c3-b9'}).text
                            bot.send_message(call.chat.id, text=f'<a href="{img_url}">&#8203;</a><b>Наименование:</b> {name} \n<b>Цена:</b> {price}\n<a href=\"{url}\"><b>Ссылка</b></a>',parse_mode='html')
                        except:
                            print('ERROR')
                            continue
                    owb(call)
        else:
            for card in cards:
                try:
                    get_image = card.find(class_='hy7').img.get('src')
                    img_url = get_image
                    get_url = card.find(class_='tile-hover-target h2y hy3').get('href')
                    url = f'https://ozon.ru{get_url}'
                    name = card.find(class_='xd3 d4x x4d h2y hy3').text
                    price = card.find('span', {'class': 'c3-a1 tsHeadline500Medium c3-b9'}).text
                    bot.send_message(call.chat.id, text=f'<a href="{img_url}">&#8203;</a><b>Наименование:</b> {name} \n<b>Цена:</b> {price}\n<a href=\"{url}\"><b>Ссылка</b></a>',parse_mode='html')
                except:
                    print('ERROR')
                    continue
            owb(call)
    else:
        for card in cards:
            try:
                get_image = card.find(class_='hy7').img.get('src')
                img_url = get_image
                get_url = card.find(class_='tile-hover-target h2y hy3').get('href')
                url =  f'https://ozon.ru{get_url}'
                name = card.find(class_='xd3 d4x x4d h2y hy3').text
                price = card.find('span', {'class': 'c3-a1 tsHeadline500Medium c3-b9'}).text
                bot.send_message(call.chat.id, text=f'<a href="{img_url}">&#8203;</a><b>Наименование:</b> {name} \n<b>Цена:</b> {price}\n<a href=\"{url}\"><b>Ссылка</b></a>',parse_mode='html')
            except:
                print('ERROR')
                continue
        owb(call)
    

    driver.close()
    driver.quit()
    


bot.infinity_polling()
# https://www.ozon.ru/search/?text=палвлва&from_global=true
# https://www.wildberries.ru/catalog/0/search.aspx?search=ffdafdsf