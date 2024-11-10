import telebot
from telebot import types
import time

class user_time: #класс, содержащий данные о удобном для пользователя времени
    
    message_time_morning = ''
    message_time_evening = ''

    def __init__(self):
        pass
    

bot = telebot.TeleBot('7540882179:AAHlHSHct3g2ic2Y8_YI4aozsuEz9K5tjgs')

@bot.message_handler(content_types=['text'])

def first_contact(message):
    if (message.text == 'Привет!') or (message.text == '/start'):
        user_time()
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item=types.KeyboardButton('Кто ты? 😯')
        markup.add(item)
        bot.send_message(message.chat.id,'Привет!',reply_markup=markup)
        bot.register_next_step_handler(message, first_contact)
            
    else:
        bot.send_message(message.from_user.id, 'Напиши "Привет!" или "/start"')

bot.infinity_polling()