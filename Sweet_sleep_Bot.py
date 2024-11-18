import telebot
from telebot import types
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

# Инициализация планировщика
scheduler = BackgroundScheduler()
scheduler.start()

# Словарь для хранения данных пользователей
users = {}

# Структура, хранящая данные о пользователе
class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.message_time_morning = None
        self.message_time_evening = None
        self.survey_data = []
        self.tips_received = []
        self.tips_sent = 0
        self.survey_in_progress = False
        self.current_survey_step = 0
        self.current_survey_data = {}

bot = telebot.TeleBot('7923436690:AAEzJNJFD9TmW92pYr1be-Uhh_qXfE8hc5M')

# Удаляем вебхук перед началом polling
bot.remove_webhook()

@bot.message_handler(commands=['start'])
def start(message):
    first_contact(message)

# Первая, главная функция программы. В ней прописан "первый контакт" с ботом, а также условия, необходимые для работы той или иной функции бота
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
        bot.register_next_step_handler(message, information)
    elif message.text == '/menu':
        menu(message)
    elif message.text == 'Да' or message.text == 'Нет':
        survey_handler(message)
    else:
        user = users.get(chat_id)
        if user is None:
            bot.send_message(message.chat.id, 'Напиши "Привет!" или "/start"')
        else:
            bot.send_message(message.chat.id, 'Напиши "/menu"')
        bot.register_next_step_handler(message, first_contact)

# Функция, в которой описан первый диалог с ботом, знакомство с ним
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

# Функция для проверки правильности формата введённого времени
def valid_time_format(time_str):
    try:
        time.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

# Первыя из двух функций для установки времени отправки ботом сообщений
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

# Вторая функция для установки времени отправки ботом сообщений
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

# Функция для сохранения выбранного пользователем времени 
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

# Фунция установки времени отправи сообщений для бота
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

# Начальная функция для отправки пользователю утренего сообщения
def send_morning_message(chat_id):
    user = users.get(chat_id)
    if user:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item_yes = types.KeyboardButton('Да')
        item_no = types.KeyboardButton('Нет')
        markup.add(item_yes, item_no)
        bot.send_message(chat_id, 'Привет! Лови утреннюю анкету 😊\nВы готовы пройти анкету?', reply_markup=markup)

# Функция для обработаки ответа пользователя
def survey_handler(message):
    chat_id = message.chat.id
    user = users[chat_id]
    if message.text == 'Да':
        user.current_survey_step = 1
        user.current_survey_data = {}
        ask_survey_question(message)
    else:
        bot.send_message(chat_id, 'Хорошо, может в следующий раз!')
        user.survey_in_progress = False

# Функция для проведения опроса
def ask_survey_question(message):
    chat_id = message.chat.id
    user = users[chat_id]
    if user.current_survey_step == 1:
        bot.send_message(chat_id, 'Время подъема (часы):')
        bot.register_next_step_handler(message, survey_response)
    elif user.current_survey_step == 2:
        bot.send_message(chat_id, 'Время подъема (минуты):')
        bot.register_next_step_handler(message, survey_response)
    elif user.current_survey_step == 3:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item1 = types.KeyboardButton('👍')
        item2 = types.KeyboardButton('👌')
        item3 = types.KeyboardButton('👎')
        markup.add(item1, item2, item3)
        bot.send_message(chat_id, 'Оцени легкость подъема', reply_markup=markup)
        bot.register_next_step_handler(message, survey_response)
    elif user.current_survey_step == 4:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item1 = types.KeyboardButton('Быстро')
        item2 = types.KeyboardButton('Средне')
        item3 = types.KeyboardButton('Долго')
        markup.add(item1, item2, item3)
        bot.send_message(chat_id, 'Быстро получилось заснуть?', reply_markup=markup)
        bot.register_next_step_handler(message, survey_response)
    elif user.current_survey_step == 5:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item1 = types.KeyboardButton('😀')
        item2 = types.KeyboardButton('😊')
        item3 = types.KeyboardButton('😐')
        item4 = types.KeyboardButton('😒')
        item5 = types.KeyboardButton('😖')
        markup.add(item1, item2, item3, item4, item5)
        bot.send_message(chat_id, 'Как твой настрой на день?', reply_markup=markup)
        bot.register_next_step_handler(message, survey_response)
    elif user.current_survey_step == 6:
        bot.send_message(chat_id, 'Супер! Крутого тебе дня 🤩')
        # Сохраняем данные анкеты
        user.survey_data.append(user.current_survey_data)
        user.survey_in_progress = False
        bot.send_message(chat_id, 'Если хотите посмотреть меню, напишите /menu')

# Функция для сохранения полученных их опроса данный. а также для логического следования опроса
def survey_response(message):
    chat_id = message.chat.id
    user = users[chat_id]
    step = user.current_survey_step
    response = message.text
    if step == 1:
        if response.isdigit() and 0 <= int(response) and int(response) <= 23:
            user.current_survey_data['wake_hour'] = int(response)
            user.current_survey_step += 1
            ask_survey_question(message)
        else:
            bot.send_message(chat_id, 'Пожалуйста, введите час в формате от 0 до 23.')
            bot.register_next_step_handler(message, survey_response)
    elif step == 2:
        if response.isdigit() and 0 <= int(response) and int(response) <= 59:
            user.current_survey_data['wake_minute'] = int(response)
            user.current_survey_step += 1
            ask_survey_question(message)
        else:
            bot.send_message(chat_id, 'Пожалуйста, введите минуты в формате от 0 до 59.')
            bot.register_next_step_handler(message, survey_response)
    elif step == 3:
        if response in ['👍', '👌', '👎']:
            user.current_survey_step += 1
            ask_survey_question(message)
        else:
            bot.send_message(chat_id, 'Пожалуйста, выберите один из вариантов.')
            bot.register_next_step_handler(message, survey_response)
    elif step == 4:
        if response in ['Быстро', 'Средне', 'Долго']:
            user.current_survey_step += 1
            ask_survey_question(message)
        else:
            bot.send_message(chat_id, 'Пожалуйста, выберите один из вариантов.')
            bot.register_next_step_handler(message, survey_response)
    elif step == 5:
        if response in ['😀', '😊', '😐', '😒', '😖']:
            user.current_survey_step += 1
            ask_survey_question(message)
        else:
            bot.send_message(chat_id, 'Пожалуйста, выберите один из вариантов.')
            bot.register_next_step_handler(message, survey_response)

# Функция для оправки вечернего сообщения
def send_evening_message(chat_id):
    user = users.get(chat_id)
    if user and user.tips_sent < 5:
        tip = get_sleep_tip(user.tips_sent)
        bot.send_message(chat_id, f'Совет для сна: \n{tip}')
        user.tips_received.append(tip)
        user.tips_sent += 1
        bot.send_message(chat_id, 'Если хотите посмотреть меню, напишите /menu')
    else:
        bot.send_message(chat_id, 'Советы кончились. Но скоро будут обновления!')

# Функция для выбора совета для вечернего сообщения
def get_sleep_tip(index):
    tips = [
        "Совет 1: Избегайте употребления кофеина перед сном.",
        "Совет 2: Поддерживайте регулярный график сна.",
        "Совет 3: Создайте комфортную обстановку для сна.",
        "Совет 4: Избегайте использования гаджетов перед сном.",
        "Совет 5: Расслабьтесь перед сном с помощью медитации или чтения."
    ]
    if index < len(tips):
        return tips[index]
    else:
        return "Нет дополнительных советов."

# Меню
@bot.message_handler(commands=['menu'])
def menu(message):
    chat_id = message.chat.id
    user = users.get(chat_id)
    if user is None:
        bot.send_message(chat_id, 'Пожалуйста, напишите "Привет!" или "/start" чтобы начать.')
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Получить статистику сна')
        item2 = types.KeyboardButton('Посмотреть библиотеку полученных советов для сна')
        item3 = types.KeyboardButton('Поменять желаемое время получения сообщений')
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(chat_id, 'Выберите действие:', reply_markup=markup)
        bot.register_next_step_handler(message, menu_selection)

# Выбор пунктов меню. Выполнение соответствующих действий
def menu_selection(message):
    chat_id = message.chat.id
    user = users.get(chat_id)
    if message.text == 'Получить статистику сна':
        stats = get_sleep_statistics(user)
        bot.send_message(chat_id, stats)
        bot.register_next_step_handler(message, menu_selection)
    elif message.text == 'Посмотреть библиотеку полученных советов для сна':
        tips = '\n'.join(user.tips_received)
        if tips:
            bot.send_message(chat_id, 'Ваши советы для сна:\n' + tips)
        else:
            bot.send_message(chat_id, 'Вы еще не получили ни одного совета.')
        bot.register_next_step_handler(message, menu_selection)
    elif message.text == 'Поменять желаемое время получения сообщений':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item=types.KeyboardButton('Начнём')
        markup.add(item)
        bot.send_message(chat_id, 'Давайте настроим время снова.',reply_markup=markup)
        bot.register_next_step_handler(message, chose_time)
    else:
        bot.send_message(chat_id, 'Пожалуйста, выберите один из вариантов.')
        bot.register_next_step_handler(message, menu_selection)

# Получение статистики о пользователе для её дальнейшего вывода
def get_sleep_statistics(user):
    if not user.survey_data:
        return 'У вас пока нет данных для статистики.'
    else:
        total_entries = len(user.survey_data)
        stats = f'Вы прошли анкету {total_entries} раз(а).\n'

        #расчет среднего времени подъема
        wake_times = [d['wake_hour'] * 60 + d['wake_minute'] for d in user.survey_data]
        avg_wake_time = sum(wake_times) / total_entries
        avg_hour = int(avg_wake_time // 60)
        avg_minute = int(avg_wake_time % 60)
        stats += f'Среднее время подъема: {avg_hour:02d}:{avg_minute:02d}\n'

        return stats

bot.infinity_polling()