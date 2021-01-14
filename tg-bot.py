#!/usr/bin/env python
# --coding:utf-8--

import telebot
from telebot import types
from setting import mytokin, tokinOWM

import pyowm

bot = telebot.TeleBot(mytokin)

age = 0
em_status = {
	'ясно':'☀',
	'пасмурно':'☁',
	'снег':'🌨',
	'проливной дождь':'🌨',
	'небольшая облачность':'🌤',
	'небольшая морось':'💧',
	'переменная облачность':'⛅',
	'небольшой дождь':'☔',
	'облачно с прояснениями':'🌥',
	'мгла':'🌫',
	'небольшой снег':'❄',
	'небольшой снегопад':'🌨',
	'туман':'🌫',
}

@bot.message_handler(content_types=['text'])
def start(message):
	if message.text == '/reg':
		bot.send_message(message.from_user.id, "Привет, " + message.from_user.first_name + "! Я Хлоя. Назовите любой город, чтобы узнать какая сейчас там погода?")
		bot.register_next_step_handler(message, get_weatherbot) #следующий шаг – функция get_name
	else:
		bot.send_message(message.from_user.id, 'Напиши /reg')

def get_weatherbot(place): #получаем город
	owm = pyowm.OWM(tokinOWM, language = 'ru')

	try:
		observation = owm.weather_at_place(place.text)
		weather = observation.get_weather()

		temp = weather.get_temperature('celsius')['temp']
		status = weather.get_detailed_status()
		wind = weather.get_wind()['speed']
		humidity = weather.get_humidity()


		bot.send_message(place.from_user.id, 'В городе '+ place.text +' сейчас '+ status + ' ' + em_status[status]+ '\n' + '🌡 Температура в городе '+ str(temp) + ' C°' + '\n' + '💨 Ветер - ' + str(wind)+ ' м/с' + '\n' + '💧 Влажность - ' + str(humidity) + '%')

		if temp < -15:
			bot.send_message(place.from_user.id, 'Брр... Сейчас очень холодно. Лучше останьтесь дома, попейте горячего чаю ☕')
		elif temp < 10:
			bot.send_message(place.from_user.id, 'Сейчас холодно. Одевайтесь потеплее! Хлоя заботится о вашем здоровье ❤')
		elif temp < 20:
			bot.send_message(place.from_user.id, 'Сейчас прохладно. Оденьтесь ☺')
		elif temp > 35:
			bot.send_message(place.from_user.id, 'Сейчас очень жарко. Лучше побудьте дома! 🏠')
		elif temp > 25:
			bot.send_message(place.from_user.id, 'Сейчас отличная летняя погода. Может быть искупаемся? 🏊')
		else:
			bot.send_message(place.from_user.id, 'Сегодня тепло. Оденьтесь полегче 🤗')
	except pyowm.exceptions.api_response_error.NotFoundError:
		bot.send_message(place.from_user.id, 'Я не могу найти Ваш город. Вы точно всё правильно написали? Попробуйте ещё раз. Нажмите /reg')
	bot.register_next_step_handler(place, start)


def get_name(name): #получаем фамилию
	bot.send_message(name.from_user.id, 'Какая у тебя фамилия?')
	bot.register_next_step_handler(name, get_surname)

def get_surname(surname):
	bot.send_message(surname.from_user.id, 'Сколько тебе лет?')
	bot.register_next_step_handler(surname, get_age)

def get_age(message):
	global age
	while age == 0: #проверяем что возраст изменился
		try:
			age = int(message.text) #проверяем, что возраст введен корректно
		except Exception:
			bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
	keyboard = types.InlineKeyboardMarkup() #наша клавиатура
	key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes') #кнопка «Да»
	keyboard.add(key_yes) #добавляем кнопку в клавиатуру
	key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
	keyboard.add(key_no)
	question = 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+'?'
	bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	if call.data == "yes": 
		#call.data это callback_data, которую мы указали при объявлении кнопки
		#код сохранения данных, или их обработки
		bot.send_message(call.message.chat.id, 'Запомню :)')
	elif call.data == "no":
		bot.send_message(call.message.chat.id, 'Напиши /reg')

bot.polling(none_stop=True, interval=0)