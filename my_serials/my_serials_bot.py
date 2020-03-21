import tmdbsimple as tmdb
import telebot

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_django_project.settings")
django.setup()

# from your_project_path import settings as your_project_settings
# from django.core.management import settings

from my_serials.models import Serial, User
from my_serials.views import serial_info

tmdb.API_KEY = '71af347ad6265c67d36f595aa27ea28c'


bot = telebot.TeleBot('1011249006:AAEEWYV0BqIrRkHkLMt2rT-wztmr5nXRHa0')

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('On Air Today', 'Chat Id', 'My Serials')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Welcome to MySerial Bot!\nUse buttons below', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'On Air Today':
        tv = tmdb.TV()
        air_today = tv.airing_today()['results']
        text_message = 'On Air Today:\n'
        for elem in air_today:
            text = '{} ({})\n'.format(elem['name'], elem['first_air_date'][:4])
            text_message += text
        bot.send_message(message.chat.id, text_message)

    if message.text == 'Chat Id':
        bot.send_message(message.chat.id, message.chat.id)

    if message.text == 'My Serials':
        user = User.objects.get(id=1)
        serial_list = Serial.objects.filter(owner=user).order_by('title')
        text_message = '<u>My Serials:</u>\n'
        for elem in serial_list:
            tv = serial_info(elem.serial_id)
            if tv.get('next_overview'):
                text = "<b>{} ({})</b>\n".format(tv['name'], tv['first_air_date'][:4])
                text_message += text
                text = "<i>{} {}</i>\n{}\n\n".format(tv['next_date'], tv['next_name'], tv['next_overview'])
                text_message += text
        bot.send_message(message.chat.id, text_message, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)





