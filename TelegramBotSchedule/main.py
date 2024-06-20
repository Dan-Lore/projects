import telebot
import requests
import datetime
import json
import math


api_key = ''
api_key_ow = ''
with open('data.json', 'r') as file:
    data = json.load(file)
    api_key = data.get('API_KEY')
    api_key_ow = data.get('API_KEY_OW')
bot = telebot.TeleBot(api_key)

# Словарь для хранения списка задач в формате {уникальный_номер: {date: 'дата', 'task': 'текст_задачи', 'completed': False}}
scheduled_tasks = {}
task_counter = 1

code_to_smile = {
     "Clear": "Ясно \U00002600",
     "Clouds": "Облачно \U00002601",
     "Rain": "Дождь \U00002614",
     "Drizzle": "Дождь \U00002614",
     "Thunderstorm": "Гроза \U000026A1",
     "Snow": "Снег \U0001F328",
     "Mist": "Туман \U0001F32B"
}

commands = {
        '/add_task': 'ДД-ММ-ГГГГ Новая задача - для добавления новой задачи',
        '/last_tasks': ' - для просмотра 10 последних задач',
        '/today_tasks': ' - для просмотра задач на сегодня',
        '/complete_task': ' Номер_задачи - для отметки задачи как выполненной',
        '/delete_task': ' Номер_задачи - для удаления задачи из списка',
        '/weather': ' Название_города - для просмотра текущей погоды(вернёт погоду для Владивостока, если не ввести город)'
}

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, 'Привет! Я бот для составления списка задач. Используй /help для просмотра списка команд управления.')

@bot.message_handler(commands=['help'])
def handle_help(message):
    global commands
    reply_text = 'Доступные команды:\n'
    for command, description in commands.items():
        reply_text += f"{command} {description}\n"
    bot.reply_to(message, reply_text)

@bot.message_handler(commands=['add_task'])
def handle_add_scheduled_task(message):
    global task_counter
    try:
        command, date_str, task_text = message.text.split(' ', 2)
        date = datetime.datetime.strptime(date_str, '%d-%m-%Y').date()
        today = datetime.date.today()
        if date < today:
            bot.reply_to(message, 'Вы не можете добавлять задачи в прошлое.')
        else:
            scheduled_tasks[task_counter] = {'date': date, 'task': task_text, 'completed': False}
            task_counter += 1
            bot.reply_to(message, f'Добавлена новая задача ({date.strftime("%d-%m-%Y")} №{task_counter-1}): {task_text}')
    except ValueError:
        bot.reply_to(message, 'Пожалуйста, используйте команду в формате /add_task ДД-ММ-ГГГГ Новая задача.')

@bot.message_handler(commands=['last_tasks'])
def handle_last_tasks(message):
    today = datetime.date.today()
    last_10_tasks = sorted(scheduled_tasks.items(), key=lambda x: x[0], reverse=True)[:10]
    tasks_to_show = [f'({task_data["date"].strftime("%d-%m-%Y")} №{task_number}): {task_data["task"]} {"✅" if task_data["completed"] else ""}' for task_number, task_data in last_10_tasks]
    if tasks_to_show:
        reply_text = 'Последние задачи:\n' + '\n'.join(tasks_to_show)
    else:
        reply_text = 'Пока нет запланированных задач.'
    bot.reply_to(message, reply_text)

@bot.message_handler(commands=['today_tasks'])
def handle_tasks_for_today(message):
    today = datetime.date.today()
    tasks_today = [f'({task_number}): {task_data["task"]} {"✅" if task_data["completed"] else ""}' for task_number, task_data in scheduled_tasks.items() if task_data["date"] == today]
    if tasks_today:
        reply_text = f'Задачи на сегодня ({today.strftime("%d-%m-%Y")}):\n' + '\n'.join(tasks_today)
    else:
        reply_text = 'На сегодня задач нет.'
    bot.reply_to(message, reply_text)

@bot.message_handler(commands=['complete_task'])
def handle_complete_task(message):
    try:
        command, task_number_str = message.text.split()
        task_number = int(task_number_str)
        if task_number in scheduled_tasks:
            scheduled_tasks[task_number]['completed'] = True
            bot.reply_to(message, f'Задача ({scheduled_tasks[task_number]["date"].strftime("%d-%m-%Y")} №{task_number}): "{scheduled_tasks[task_number]["task"]}" отмечена как выполненная.')
        else:
            bot.reply_to(message, 'Задача не найдена. Проверьте ввод.')
    except (ValueError, KeyError):
        bot.reply_to(message, 'Пожалуйста, используйте команду в формате /complete_task НОМЕР_ЗАДАЧИ.')

@bot.message_handler(commands=['delete_task'])
def handle_delete_task(message):
    try:
        command, task_number_str = message.text.split()
        task_number = int(task_number_str)
        if task_number in scheduled_tasks:
            del scheduled_tasks[task_number]
            bot.reply_to(message, f'Задача (№{task_number} удалена.')
        else:
            bot.reply_to(message, 'Задача не найдена. Проверьте ввод.')
    except (ValueError, KeyError):
        bot.reply_to(message, 'Пожалуйста, используйте команду в формате /delete_task НОМЕР_ЗАДАЧИ.')

@bot.message_handler(commands=['weather'])
def get_weather(message):
    try:
        try:
            command, city = message.text.split()
        except ValueError:
            city = 'Владивосток'
        global api_key_ow
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid={api_key_ow}")
        data = response.json()
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        
        # получаем значение погоды
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            # если эмодзи для погоды нет, выводим другое сообщение
            wd = "Посмотри в окно, я не понимаю, что там за погода..."

        # продолжительность дня
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        
        reply_text = (f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}\n"
                    f"Погода в городе: {city}\nТемпература: {cur_temp}°C {wd}\n"
                    f"Влажность: {humidity}%\nДавление: {math.ceil(pressure/1.333)} мм.рт.ст\nВетер: {wind} м/с \n"
                    f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                    f"Хорошего дня!")
        bot.reply_to(message, reply_text)
    except:
        bot.reply_to(message, "ОШИБКА!")

bot.set_my_commands(commands)
bot.polling()