#!/usr/bin/env python
# --coding:utf-8--

import time
import telebot
from telebot import types
from setting import mytokin, channel_login, sleep_bot

bot = telebot.TeleBot(mytokin)

text_for_channel = 'Привет, не забудьте про дни рождения в январе:\n 04.01 - Игорь Ромащенко;\n 09.01 - Нина Гогаева;\n 25.01 - Анастасия Гулимова!'

for channel in channel_login:
	bot.send_message(channel, text_for_channel)
	time.sleep(int(sleep_bot))