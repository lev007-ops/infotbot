#!/usr/bin/env python3
import telebot
from telebot import types
import config


client = telebot.TeleBot(config.CONFIG['token'])


#стартовое сообщение
@client.message_handler(commands=['start'])
def welcom(message):
    hello_text = '''Привет!
Я info bot, напиши команду: "/info"'''
    client.send_message(message.chat.id, hello_text)


@client.message_handler(commands=['get_info', 'info'])


def get_user_info(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text = 'Да✅', callback_data='yes')
    item_no = types.InlineKeyboardButton(text = 'Нет❌', callback_data='no')
    markup_inline.add(item_yes, item_no)
    chat_id = message.chat.id
    client.send_message(chat_id, 'Получить инфу?', reply_markup=markup_inline)


@client.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'yes':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_id = types.KeyboardButton('Moй Id')
        item_username = types.KeyboardButton('Moй ник')
        markup_reply.add(item_id, item_username)
        reply = "Нажмите на кнопку для получения информации"
        chat_id = call.message.chat.id
        client.send_message(chat_id, reply, reply_markup=markup_reply)

    elif call.data == 'no':
        client.send_message(call.message.chat.id, 'В другой раз')


@client.message_handler(content_types=['text'])
def get_text(message):
    if message.text == 'Moй Id':
        client.send_message(message.chat.id, f'Ваш Id: {message.from_user.id}')
    elif message.text == 'Moй ник':
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        reply_text = f'Ваш ник: {first_name} {last_name}'
        client.send_message(message.chat.id, reply_text)


client.polling(none_stop=True, interval=0)

