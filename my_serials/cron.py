import telebot
import schedule
import time

bot = telebot.TeleBot('1011249006:AAEEWYV0BqIrRkHkLMt2rT-wztmr5nXRHa0')


def send_text():
    bot.send_message(415552649, 'Hello from Win cron!', parse_mode='HTML')
