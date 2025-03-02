import telebot
import requests
import threading
import time
import gspread
from google.oauth2.service_account import Credentials

TELEGRAM_BOT_TOKEN = "7841693985:AAE5Kt19ek3tmAGg6wXiTWy2867ZbqgkcPE"
WEATHER_API_KEY = "6c7e3db77edfd1d56eb3ae377ba89ce3"
SPREADSHEET_ID = "1gpxCyi4uyFQZIXzxZpB5FMkiny_T739edjOxfjC7S64"
RANGE_NAME = "Sheet1!A:D"
CREDENTIALS_FILE = r"C:\Users\xrect\PycharmProjects\pythonProject2\bot11111-452510-4f0f8fb6fc3c.json"

def get_google_sheet_service():
    creds = Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    client = gspread.authorize(creds)
    return client

def write_to_sheet(reminder_message, days, hours, minutes, seconds):
    try:
        client = get_google_sheet_service()
        sheet = client.open_by_key(SPREADSHEET_ID).sheet1
        row = [reminder_message, days, hours, minutes, seconds]
        sheet.append_row(row)
    except Exception as e:
        print(f"Помилка при додаванні до таблиці: {e}")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

reminders = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     '*Привіт! Я Den4ik_bot!* 👋\n'
                     'Я можу допомогти вам з нагадуваннями, погоди та іншими функціями.\n\n'
                     '_Використовуйте команди:_\n'
                     '/start - старт\n'
                     '/help - допомога\n'
                     '/weather <місто> - отримати прогноз погоди\n'
                     '/remind - створити нагадування', parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                     '*Команди бота:*\n\n'
                     '/start - Почати взаємодію з ботом.\n'
                     '/help - Показати список команд.\n'
                     '/weather <місто> - Отримати прогноз погоди для міста.\n'
                     '/remind - Створити нагадування на певний час.\n', parse_mode='Markdown')

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    if data.get("cod") != 200:
        return "❌ Помилка: Місто не знайдено!"
    temp = data['main']['temp']
    description = data['weather'][0]['description']
    return f'Температура: {temp}°C, Стан: {description}'

@bot.message_handler(commands=['remind'])
def remind(message):
    bot.send_message(message.chat.id, "⚠️ Що вам потрібно нагадати? Напишіть повідомлення.")
    bot.register_next_step_handler(message, get_reminder_message)

def get_reminder_message(message):
    reminder_message = message.text
    reminders[message.chat.id] = {'message': reminder_message}
    bot.send_message(message.chat.id, "⏳ Скільки часу ви хочете почекати перед нагадуванням? Вкажіть:\n"
                                      "*Скільки днів?* (Введіть число)", parse_mode='Markdown')
    bot.register_next_step_handler(message, get_days)

def get_days(message):
    try:
        days = int(message.text)
        reminders[message.chat.id]['days'] = days
        bot.send_message(message.chat.id, f"Дні: {days}. Скільки годин? (Введіть число)")
        bot.register_next_step_handler(message, get_hours)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Будь ласка, введіть число для днів.", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_days)

def get_hours(message):
    try:
        hours = int(message.text)
        reminders[message.chat.id]['hours'] = hours
        bot.send_message(message.chat.id, f"Години: {hours}. Скільки хвилин? (Введіть число)")
        bot.register_next_step_handler(message, get_minutes)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Будь ласка, введіть число для годин.", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_hours)

def get_minutes(message):
    try:
        minutes = int(message.text)
        reminders[message.chat.id]['minutes'] = minutes
        bot.send_message(message.chat.id, f"Хвилини: {minutes}. Скільки секунд? (Введіть число)")
        bot.register_next_step_handler(message, get_seconds)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Будь ласка, введіть число для хвилин.", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_minutes)

def get_seconds(message):
    try:
        seconds = int(message.text)
        reminders[message.chat.id]['seconds'] = seconds

        total_time = (reminders[message.chat.id]['days'] * 24 * 60 * 60) + \
                     (reminders[message.chat.id]['hours'] * 60 * 60) + \
                     (reminders[message.chat.id]['minutes'] * 60) + \
                     reminders[message.chat.id]['seconds']

        bot.send_message(message.chat.id,
                         f"✅ Нагадування створено!\n"
                         f"Ви отримаєте нагадування через *{reminders[message.chat.id]['days']} дні(в), "
                         f"{reminders[message.chat.id]['hours']} годин(и), "
                         f"{reminders[message.chat.id]['minutes']} хвилин(и), "
                         f"{reminders[message.chat.id]['seconds']} секунд*.",
                         parse_mode='Markdown')

        reminder_thread = threading.Thread(target=send_reminder_after_time, args=(message.chat.id, total_time))
        reminder_thread.start()

    except ValueError:
        bot.send_message(message.chat.id, "❌ Будь ласка, введіть число для секунд.", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_seconds)

def send_reminder_after_time(chat_id, total_time):
    time.sleep(total_time)
    bot.send_message(chat_id, reminders[chat_id]['message'])

@bot.message_handler(commands=['weather'])
def weather(message):
    city = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else ""
    if city:
        weather_info = get_weather(city)
        bot.send_message(message.chat.id, weather_info)
    else:
        bot.send_message(message.chat.id, "Будь ласка, вкажіть місто. Використовуйте: /weather <місто>")

@bot.message_handler(commands=['stop'])
def stop(message):
    bot.send_message(message.chat.id, '🛑 Бот зупинено.')
    bot.stop_polling()

bot.polling(none_stop=True)
