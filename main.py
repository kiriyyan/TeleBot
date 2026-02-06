import json
from http.client import responses

from config import API_TOKEN
import telebot
import subscribe
from subscribe import ADMIN_ID, load_user_set
import time
import AI
from values import take_usd_to_rub, take_eur_to_rub, take_last_news

bot = telebot.TeleBot(API_TOKEN)



@bot.message_handler(commands = ['start', 'help'])
def handle_start(message):
    subscribe.set_user(message)
    # set_user_info(message)
    print(message.chat)
    bot.send_message(message.chat.id, f'Привет, {message.chat.first_name}')
    print(f"[{message.chat.first_name}]: /start")

@bot.message_handler(commands=['ad'])
def send_ad(message):
    print(message.chat.id)
    if(message.chat.id == subscribe.ADMIN_ID):
        if len(message.text)>=4:

            for n in list(load_user_set()):
                bot.send_message(chat_id = n, text = message.text[4:])
                time.sleep(0.5)
            print(f'[ADMIN]: {message.text[4:]}')
        else:
            bot.send_message(message.chat.id, text = "Напишите сообщение для рассылки")
    else:
        bot.send_message(message.chat.id,'Для команды требуются права администратора')

@bot.message_handler(commands = ['usd'])
def usd_handler(message):
    bot.reply_to(message, f"USD: {take_usd_to_rub():} EUR:  {take_eur_to_rub()}\n{take_last_news()}")
    print(f"[{message.chat.first_name}]: /usd")

@bot.message_handler(content_types=['photo', 'animation'])
def handler_photo(message):
    bot.reply_to(message, 'nice meme')
    print(f"[{message.chat.first_name}]: Send photo")

@bot.message_handler(content_types=['text'])
def text_handler(message):
    print(f"[{message.chat.first_name}]: {message.text}")
    bot_response = AI.ai_response(message.text)
    bot.send_message(message.chat.id, bot_response)
    print(f"[BOT]: {bot_response}")





bot.polling(non_stop=True)