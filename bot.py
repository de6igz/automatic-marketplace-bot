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
    if message.text == 'Я покупатель':
        show_categories(message)
    if message.text == 'Назад в главное меню':
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=buyer_or_seller_markup)


def show_categories(message):
    categoris = types.ReplyKeyboardMarkup(resize_keyboard=True)
    categoris.add('Назад в главное меню', 'Верхняя одежда', 'Нижняя одежда', 'Обувь')
    bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=categoris)


def seller_menu(message):
    seller_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    seller_menu_markup.add('Назад в главное меню', 'Мои анкеты', 'Создать новую анкету')
    bot.send_message(message.chat.id, 'Добро пожаловать обратно', reply_markup=seller_menu_markup)


bot.infinity_polling()
