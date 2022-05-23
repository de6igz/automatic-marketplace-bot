import re

import telebot
from telebot import types
import sqlite3
import gitignore.tokens

bot = telebot.TeleBot(gitignore.tokens.token)

sqlite_connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = sqlite_connection.cursor()
sqlite_connection.commit()
temp_user_form_description = {}


@bot.message_handler(commands=['start'])
def start(message):
    temp_user_form_description[message.from_user.id] = 'temp'
    buyer_or_seller_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buyer_or_seller_markup.add('Я покупатель', 'Я продавец')
    bot.send_message(message.chat.id,
                     '<b><i>Привет!</i></b>\n На данной площадке ты сможешь выставлять на продажу любые вещи',
                     parse_mode='HTML', reply_markup=buyer_or_seller_markup)


@bot.message_handler(content_types=['text'])
def main(message):
    buyer_or_seller_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buyer_or_seller_markup.add('Я покупатель', 'Я продавец')
    if message.text == 'Я продавец':
        seller_menu(message)
    if message.text == 'Создать новую анкету':
        creating_form(message)
    if message.text == 'Я покупатель':
        show_buyer_categories(message)
    if message.text == 'Назад в главное меню':
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=buyer_or_seller_markup)
    if message.text == 'Мои анкеты':
        show_my_products(message)


def show_my_products(message):
    user_id = str(message.from_user.id)
    cursor.execute(f"select description from products where product_ID like '%{user_id}%'")
    my_products = cursor.fetchall()
    counter = 1
    for row in my_products:
        img = open(f'products/image_{user_id}_{counter}.jpg', 'rb')
        bot.send_message(message.chat.id, f'{row[0]}')
        bot.send_photo(message.chat.id, img)
        counter = counter + 1


def show_buyer_categories(message):
    categoris = types.ReplyKeyboardMarkup(resize_keyboard=True)
    categoris.add('Назад в главное меню', row_width=1)
    categoris.add('Верхняя одежда', 'Нижняя одежда', 'Обувь', row_width=3)
    bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=categoris)


def seller_menu(message):
    seller_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    seller_menu_markup.add('Назад в главное меню', 'Мои анкеты', 'Создать новую анкету')
    bot.send_message(message.chat.id, 'Добро пожаловать обратно', reply_markup=seller_menu_markup)


def creating_form(message):
    creating_form_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    creating_form_markup.add('Назад в главное меню', row_width=1)
    creating_form_markup.add('Верхняя одежда', 'Нижняя одежда', 'Обувь', row_width=3)
    msg = bot.send_message(message.chat.id, 'Выбери категорию', reply_markup=creating_form_markup)
    bot.register_next_step_handler(msg, deciding_category)


def deciding_category(message):
    buyer_or_seller_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buyer_or_seller_markup.add('Я покупатель', 'Я продавец')
    if message.text == 'Назад в главное меню':
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=buyer_or_seller_markup)
    if message.text == 'Верхняя одежда':
        creating_upwear_form(message)
    if message.text == 'Нижняя одежда':
        creating_underwear_form(message)
    if message.text == 'Обувь':
        creating_shoe_form(message)
    else:
        bot.send_message(message.chat.id, 'Не корректный ввод, попробуйте еще раз создать заявку')
        creating_form(message)


def creating_upwear_form(message):
    img = open('media/nike_hoodie.jpg', 'rb')
    bot.send_message(message.chat.id,
                     'Отправьте анкету по следующей форме: <b>\nФИО\nНик в телеграмме\nНаименование товвара\nЦена в рублях</b>\n\n<b><i>Пример анкеты:</i></b>\n',
                     parse_mode='HTML')
    bot.send_message(message.chat.id,
                     'Иванов Иван Иванович\n@rare_items_shop_bot\nNike Air Jordan 1\n15000 рублей')
    msg = bot.send_photo(message.chat.id, img)
    bot.register_next_step_handler(msg, check_form)


def check_form(message):
    form = str(message.text)
    if re.search(r'[А-Я]\w+\s[А-Я]\w+\s[А-Я]\w+\s', form):
        if re.search(r'@\w+', form):
            telegram_tag = re.search(r'@\w+', form).group(0)
            if re.search(r'\d+ рублей', form):
                msg = bot.send_message(message.chat.id, 'Теперь отправьте фото товара')
                temp_user_form_description[message.from_user.id] = form
                bot.register_next_step_handler(msg, download_picture)
            else:
                bot.send_message(message.chat.id, 'Не корректный ввод стоимости, попробуйте еще раз создать заявку')
                creating_form(message)
        else:
            bot.send_message(message.chat.id, 'Не корректный ввод телеграм ника, попробуйте еще раз создать заявку')
            creating_form(message)
    else:
        bot.send_message(message.chat.id, 'Не корректный ввод имени, попробуйте еще раз создать заявку')
        creating_form(message)
    try:
        cursor.execute(f"insert into sellers(telegram_tag) values ('{message.from_user.id}')")
        sqlite_connection.commit()
    except Exception as e:
        e


@bot.message_handler(content_types=['photo'])
def download_picture(message):
    try:
        nomer = 0
        cursor.execute(f'select number_of_products from sellers where telegram_tag like "{message.from_user.id}"')
        temp = cursor.fetchall()
        for row in temp:
            nomer = row[0]
        nomer = int(nomer)
        print(nomer, type(nomer))
        print('message.photo =', message.photo)
        fileID = message.photo[-1].file_id
        print('fileID =', fileID)
        file_info = bot.get_file(fileID)
        print('file.file_path =', file_info.file_path)
        downloaded_file = bot.download_file(file_info.file_path)
        nomer = nomer + 1
        cursor.execute(
            f'update sellers set number_of_products = {nomer} where telegram_tag like "{message.from_user.id}"')
        sqlite_connection.commit()
        with open(f"products/image_{message.from_user.id}_{nomer}.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
            new_file.close()
        cursor.execute(
            f"insert into products(description,photo_link,product_ID) values ('{temp_user_form_description[message.from_user.id]}','products/image_{message.from_user.id}_{nomer}.jpg','{message.from_user.id}_{nomer}')")
        sqlite_connection.commit()
        bot.send_message(message.chat.id, '<i>Товар успешно добавлен✅</i>', parse_mode='HTML')
    except Exception as e:
        bot.send_message(message.chat.id, 'Не корректный формат изображения')
        creating_form(message)


def creating_underwear_form(message):
    pass


def creating_shoe_form(message):
    pass


bot.infinity_polling()
