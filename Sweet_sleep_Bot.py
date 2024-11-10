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
        bot.register_next_step_handler(message, information)         
    else:
        bot.send_message(message.from_user.id, 'Напиши "Привет!" или "/start"')

def information(message):
    if message.text == 'Кто ты? 😯':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item=types.KeyboardButton('Хм, и как мы этого добьемся?')
        markup.add(item)
        bot.send_message(message.chat.id,'Я, Sweat_sleep бот, помогающий решить проблемы со сном 😴 \n \n Я научу тебя легко просыпаться, быстро засыпать и крепко спать. \n \n Со мной ты поднимешь уровень энергии, узнаешь, что такое "доброе утро", снизишь уровень тревоги и забудешь о синяках под глазами 😄',reply_markup=markup)
        bot.register_next_step_handler(message, information)
    elif message.text == 'Хм, и как мы этого добьемся?':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item=types.KeyboardButton('Понятно 😊Что во-вторых?')
        markup.add(item)
        bot.send_message(message.chat.id,'Я подхожу к решению проблемы комплексно \n \n Во-первых, я рассказываю о том, как устроен сон и что на него влияет. \n \n Внутри больше 30 уроков о сне, основанных на научных исследованиях, статьях сомнологов, книгах о сне и бесконечном опыте создателей 🙃 \n \n Уроки короткие: 3-5 минут на прочтение \n Уроки понятные: научные термины на простом языке \n Уроки веселые: мемы и шутки в каждом 😄',reply_markup=markup)
        bot.register_next_step_handler(message, information)
    elif message.text == 'Понятно 😊Что во-вторых?':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item=types.KeyboardButton('Договорились 👍')
        markup.add(item)
        bot.send_message(message.chat.id,'Во-вторых, я помогаю выстроить положительные для сна привычки и избавиться от вредных привычек. \n \n В уроках 22 привычки на утро и вечер. Выполнение хотя бы 2-3 из них регулярно поможет почувствовать себя лучше ☀️ \n \n Я буду присылать напоминания о привычках, чтобы снизить вероятность, что ты забудешь о них. \n \n Капелька дисциплины, которая не помешает 😏',reply_markup=markup)
        bot.register_next_step_handler(message, information)
    elif message.text == 'Договорились 👍':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item=types.KeyboardButton('Хорошо. Выделю время!')
        markup.add(item)
        bot.send_message(message.chat.id,'Расписание будет следующее: \n \n Вечер\n📋 вечерняя анкета\n📚 урок на 3-5 минут\n☑️ вечерний ритуал\n💤 сладкий сон\n\nУтро\n📋 утренняя анкета\n☑️ утренний ритуал\n☀️ бодрый день\n\nИтого: 10-15 минут вечером и 5-10 минут утром, чтобы наладить сон.',reply_markup=markup)
        bot.register_next_step_handler(message, information)
    else:
        bot.send_message(message.from_user.id, 'Нажми на кнопку!')
        bot.register_next_step_handler(message, information)


bot.infinity_polling()