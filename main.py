import telebot
import requests
import json
import secrets

bot = secrets.BOT_TOKEN
API = secrets.API


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton('погода', callback_data='weather')
    markup.row(btn)
    bot.send_message(message.chat.id, 'Привет. Рад видеть. Чтобы узнать погоду нажми "погода"', reply_markup=markup)

def next_click(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton('еще', callback_data='else')
    markup.row(btn)
    bot.send_message(message.chat.id, 'Если хочешь узнать еще про какой-либо город нажми "еще"')

@bot.callback_query_handler(func = lambda call: True)
def callback(call):
    bot.send_message(call.message.chat.id, 'Напиши название города')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    try:
        data = json.loads(res.text)
        weather = data['weather'][0]['main']
        wind = data['wind']['speed']
        temp = data['main']['temp']
        bot.reply_to(message, f'{city}. Температура: {temp}°C \n Скорость ветра: {wind} м/с')
        if weather.lower() == 'clouds':
            image = 'cloud-1919600_1280.png'
        elif weather.lower() == 'clear':
            image = 'sun-1296130_1280.png'
        else:
            image = 'cloud-4820504_1280.jpg'
        file = open('./'+image, 'rb')
        bot.send_photo(message.chat.id, file)
        bot.register_next_step_handler(message, next_click)
    except:
        bot.reply_to(message, ' Город указан неверно')



bot.polling(non_stop=True)