import telebot
from telebot import types
import time

class user_time: #класс, содержащий данные о удобном для пользователя времени
    
    def __init__(self):
        self.message_time_morning = ' '
        self.message_time_evening = ' '
    
    

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
        bot.register_next_step_handler(message, first_contact)

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
        bot.register_next_step_handler(message, chose_time)
    else:
        bot.send_message(message.from_user.id, 'Нажми на кнопку!')
        bot.register_next_step_handler(message, information)

flag = True
flag_again = False

def chose_time(message):
    global flag, flag_again
    if message.text == 'Хорошо. Выделю время!' or flag_again == True:
        flag_again = False
        flag = True
        bot.send_message(message.chat.id,'Давай настроим время прихода уведомлений ⏰ \n\n В какой час по Москве тебе удобно получать сообщения УТРОМ? 🌅 \n\n Пожалуйста, введи число с клавиатуры в формате NN:NN.')
        bot.register_next_step_handler(message, chose_time_2)
    else:
        bot.send_message(message.from_user.id, 'Нажми на кнопку!')
        bot.register_next_step_handler(message, chose_time)

def chose_time_2(message):
        global flag, flag_again
        if message.text[:2].isdigit() and message.text[3:].isdigit() and len(message.text) == 5 and message.text[2] == ':' and ord(message.text[0]) <= ord('2') and ord(message.text[1]) + ord(message.text[3]) + ord(message.text[4]) <= ord('9') * 3:
            if flag == True:
                user_time.message_time_morning(message.text)
                flag = False
                bot.send_message(message.chat.id,'В какой час по Москве тебе удобно получать сообщения ВЕЧЕРОМ? 🌃 \n \n Советую выбрать время за 1-2 часа до сна, чтобы успеть применить на практике информацию из урока. \n \n Пожалуйста, введи число с клавиатуры в формате NN:NN.')
                bot.register_next_step_handler(message, chose_time_2)
            else:
                user_time.message_time_evening(message.text)
                markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1=types.KeyboardButton('Сохранить✅')
                item2=types.KeyboardButton('Изменить')
                markup.add(item1, item2)
                bot.send_message(message.chat.id,'Сохранить выбранное время? \n \n 🌞 Утро - {user_time.message_time_morning} \n 🌚 Вечер - {user_time.message_time_evening}',reply_markup=markup)
                bot.register_next_step_handler(message, chose_time_2)
        else:
            bot.send_message(message.chat.id,'Введите ещё раз. Я вас не понял')
            bot.register_next_step_handler(message, chose_time_2)

        if message.text == 'Сохранить✅':
             bot.send_message(message.chat.id,'Супер. Время установлено')
        elif message.text == 'Изменить':
            flag_again = True
            bot.register_next_step_handler(message, chose_time)

bot.infinity_polling()