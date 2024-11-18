import telebot
from telebot import types
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

# Словарь для хранения данных пользователей
users = {}

class User: #класс, содержащий данные о удобном для пользователя времени
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.message_time_morning = None
        self.message_time_evening = None


bot = telebot.TeleBot('7540882179:AAHlHSHct3g2ic2Y8_YI4aozsuEz9K5tjgs')

@bot.message_handler(commands=['start'])
def start(message):
    first_contact(message)

@bot.message_handler(content_types=['text'])
def first_contact(message):
    if (message.text == 'Привет!') or (message.text == '/start'):
        chat_id = message.chat.id
        if chat_id not in users:
            users[chat_id] = User(chat_id)
        user = users[chat_id]
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item=types.KeyboardButton('Кто ты? 😯')
        markup.add(item)
        bot.send_message(chat_id,'Привет!',reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Напиши "Привет!" или "/start"')

def information(message):
    if message.text == 'Кто ты? 😯':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item=types.KeyboardButton('Хм, и как мы этого добьемся?')
        markup.add(item)
        bot.send_message(message.chat.id,'Я, Sweat_sleep бот, помогающий решить проблемы со сном 😴 \n \nЯ научу тебя легко просыпаться, быстро засыпать и крепко спать. \n \nСо мной ты поднимешь уровень энергии, узнаешь, что такое "доброе утро", снизишь уровень тревоги и забудешь о синяках под глазами 😄',reply_markup=markup)
        bot.register_next_step_handler(message, information)
    elif message.text == 'Хм, и как мы этого добьемся?':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item=types.KeyboardButton('Понятно 😊Что во-вторых?')
        markup.add(item)
        bot.send_message(message.chat.id,'Я подхожу к решению проблемы комплексно \n \nВо-первых, я рассказываю о том, как устроен сон и что на него влияет. \n \nВнутри 5 советов о сне, основанных на научных исследованиях, статьях сомнологов, книгах о сне и бесконечном опыте создателей 🙃 \n \nНа это тебе понадобится всего немного времени: минутку на прочтение \nСоветы обязательно помогут тебе улучшить свой сон!',reply_markup=markup)
        bot.register_next_step_handler(message, information)
    elif message.text == 'Понятно 😊Что во-вторых?':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item=types.KeyboardButton('Договорились 👍')
        markup.add(item)
        bot.send_message(message.chat.id,'Во-вторых, я помогаю выстроить положительные для сна привычки и избавиться от вредных привычек. \n \nСоблюдая их ты обязательно улучшишь свой сон!\n \nКапелька дисциплины, которая не помешает 😏',reply_markup=markup)
        bot.register_next_step_handler(message, information)
    elif message.text == 'Договорились 👍':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item=types.KeyboardButton('Хорошо. Выделю время!')
        markup.add(item)
        bot.send_message(message.chat.id,'Расписание будет следующее: \n \nВечер\n📋 Вечерний совет\n💤 сладкий сон\n\nУтро\n📋 утренняя анкета\n☀️ бодрый день\n\nИтого: минутку вечером и 2 минуты утром, чтобы наладить сон.',reply_markup=markup)
        bot.register_next_step_handler(message, chose_time)
    else:
        bot.send_message(message.chat.id, 'Нажми на кнопку!')
        bot.register_next_step_handler(message, information)

flag = True
flag_again = False

def valid_time_format(time_str):
    try:
        time.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def chose_time(message):
    global flag, flag_again
    chat_id = message.chat.id
    if message.text == 'Хорошо. Выделю время!' or flag_again == True or message.text == 'Начнём':
        flag_again = False
        flag = True
        bot.send_message(chat_id,'Давай настроим время прихода уведомлений ⏰ \n\nВ какой час по Москве тебе удобно получать сообщения УТРОМ? 🌅 \n\nПожалуйста, введи число с клавиатуры в формате HH:MM.')
        bot.register_next_step_handler(message, chose_time_2)
    else:
        bot.send_message(message.chat.id, 'Нажми на кнопку!')
        bot.register_next_step_handler(message, chose_time)

def chose_time_2(message):
    global flag, flag_again
    chat_id = message.chat.id
    user = users[chat_id]
    if valid_time_format(message.text):
        if flag == True:
            user.message_time_morning = message.text
            flag = False
            bot.send_message(chat_id,'В какой час по Москве тебе удобно получать сообщения ВЕЧЕРОМ? 🌃 \n \nСоветую выбрать время за 1-2 часа до сна, чтобы успеть применить на практике информацию из урока. \n \nПожалуйста, введи число с клавиатуры в формате HH:MM.')
            bot.register_next_step_handler(message, chose_time_2)
        else:
            user.message_time_evening = message.text
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton('Сохранить✅')
            item2=types.KeyboardButton('Изменить')
            markup.add(item1, item2)
            bot.send_message(chat_id,f'Сохранить выбранное время? \n \n🌞 Утро - {user.message_time_morning} \n🌚 Вечер - {user.message_time_evening}',reply_markup=markup)
            bot.register_next_step_handler(message, save_time)
    else:
        bot.send_message(chat_id,'Введите ещё раз. Я вас не понял')
        bot.register_next_step_handler(message, chose_time_2)

def save_time(message):
    global flag_again
    chat_id = message.chat.id
    user = users[chat_id]
    if message.text == 'Сохранить✅':
        bot.send_message(chat_id,'Супер. Время установлено')
        schedule_user_messages(user)
        bot.send_message(chat_id, 'Если хотите посмотреть меню, напишите /menu')
    elif message.text == 'Изменить':
        flag_again = True
        bot.register_next_step_handler(message, chose_time)
    else:
        bot.send_message(chat_id,'Пожалуйста, выберите один из вариантов.')
        bot.register_next_step_handler(message, save_time)

def schedule_user_messages(user):
    # Удаляем существующие задания для этого пользователя
    try:
        scheduler.remove_job(str(user.chat_id)+'_morning')
    except:
        pass
    try:
        scheduler.remove_job(str(user.chat_id)+'_evening')
    except:
        pass

    # Планируем утреннее сообщение
    morning_hour, morning_minute = map(int, user.message_time_morning.split(':'))
    scheduler.add_job(send_morning_message, 'cron', hour=morning_hour, minute=morning_minute, args=[user.chat_id], id=str(user.chat_id)+'_morning')

    # Планируем вечернее сообщение
    evening_hour, evening_minute = map(int, user.message_time_evening.split(':'))
    scheduler.add_job(send_evening_message, 'cron', hour=evening_hour, minute=evening_minute, args=[user.chat_id], id=str(user.chat_id)+'_evening')

def send_morning_message(chat_id):
    pass

def send_evening_message(chat_id):
    pass

bot.infinity_polling()