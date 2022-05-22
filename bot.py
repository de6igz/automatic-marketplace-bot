import telebot
from telebot import types

import gitignore.tokens

bot = telebot.TeleBot(gitignore.tokens.token)


@bot.message_handler(commands=['start'])
def start(message):
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
    if message.text == 'Верхняя одежда':
        creating_upwear_form(message)
    elif message.text == 'Нижняя одежда':
        creating_underwear_form(message)
    elif message.text == 'Обувь':
        creating_shoe_form(message)


def creating_upwear_form(message):
    bot.send_message(message.chat.id,
                     'Отправьте анкету по следующей форме: <b>\nФИО\nНаименование товвара\nЦена в рублях</b>\n<b><i>Пример анкеты</i></b>\nИванов Иван Иванович\nNike Air Jordan 1\n15000 рублей',
                     parse_mode='HTML')


def creating_underwear_form(message):
    pass


def creating_shoe_form(message):
    pass


bot.infinity_polling()
