import django
import os
import telebot
import tmdbsimple as tmdb
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_serials_project.settings")
django.setup()

from my_serials.models import Serial, User, Profile
from my_serials.views import serial_info

bot = telebot.TeleBot('1011249006:AAEEWYV0BqIrRkHkLMt2rT-wztmr5nXRHa0')

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('On Air', 'Chat Id')
keyboard1.row('My Serials', 'My Serials On Air')


def send_notification():
    profiles = Profile.objects.filter(telegram_id__isnull=False)
    for profile in profiles:
        user = User.objects.get(profile=profile)
        tv = tmdb.TV()
        serial_list = Serial.objects.filter(owner=user)
        air_today = tv.airing_today()['results']
        air_today_id_list = [tv['id'] for tv in air_today]
        my_serials_on_air = [serial for serial in serial_list if
                             serial.serial_id in air_today_id_list]
        text_message = '<u>My Serials On Air:</u>\n\n'
        if my_serials_on_air:
            for serial in my_serials_on_air:
                tv = serial_info(serial.serial_id)
                text = "<b>{} ({})</b>\n".format(tv['name'], tv['first_air_date'][:4])
                text_message += text
                if tv.get('next_overview'):
                    text = "<i>Episode: {} {}</i>\n{}\n\n".format(tv['next_episode_number'],
                                                                  tv['next_name'],
                                                                  tv['next_overview'])
                    text_message += text
            try:
                bot.send_message(profile.telegram_id, text_message, parse_mode='HTML')
            except telebot.apihelper.ApiException:
                pass


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Welcome to MySerial Bot!\n'
                     'Use buttons below',
                     reply_markup=keyboard1)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'To use full bot functionality you must get chat id'
                     ' by pushing button and enter your id '
                     'on edit profile page',
                     reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'On Air':
        tv = tmdb.TV()
        air_today = tv.airing_today()['results']
        text_message = '<u>On Air Today:</u>\n\n'
        for elem in air_today:
            text = '{} ({})\n'.format(elem['name'], elem['first_air_date'][:4])
            text_message += text
        bot.send_message(message.chat.id, text_message, parse_mode='HTML')

    if message.text == 'Chat Id':
        bot.send_message(message.chat.id,
                         'Your chat id is <b>{}</b>\n'
                         'Enter this id in your profile page'
                         .format(message.chat.id), parse_mode='HTML')

    if message.text == 'My Serials':
        try:
            profile = Profile.objects.get(telegram_id=message.chat.id)
            user = User.objects.get(profile=profile)
        except ObjectDoesNotExist:
            user = None
        if not user:
            bot.send_message(message.chat.id,
                             '<b>You are not connected to data base!</b>\n'
                             'Enter your <i>chat id</i> on edit profile page',
                             parse_mode='HTML')
        else:
            serial_list = Serial.objects.filter(owner=user).order_by('title')
            text_message = '<u>My Serials:</u>\n\n'
            for elem in serial_list:
                tv = serial_info(elem.serial_id)
                text = "<b>{} ({})</b>\n".format(tv['name'], tv['first_air_date'][:4])
                text_message += text
                if tv.get('next_overview'):
                    text = "<i>Episode: {} {} {}</i>\n{}\n\n".format(tv['next_episode_number'],
                                                                     tv['next_date'],
                                                                     tv['next_name'],
                                                                     tv['next_overview'])
                    text_message += text
                else:
                    text_message += 'Data currently unavailable\n\n'
            bot.send_message(message.chat.id, text_message, parse_mode='HTML')

    if message.text == 'My Serials On Air':
        try:
            profile = Profile.objects.get(telegram_id=message.chat.id)
            user = User.objects.get(profile=profile)
        except ObjectDoesNotExist:
            user = None
        if not user:
            bot.send_message(message.chat.id,
                             '<b>You are not connected to data base!</b>\n'
                             'Enter your <i>chat id</i> on your profile page',
                             parse_mode='HTML')
        else:
            tv = tmdb.TV()
            serial_list = Serial.objects.filter(owner=user)
            air_today = tv.airing_today()['results']
            air_today_id_list = [tv['id'] for tv in air_today]
            text_message = '<u>My Serials On Air:</u>\n\n'
            my_serials_on_air = [serial for serial in serial_list if
                                 serial.serial_id in air_today_id_list]
            if my_serials_on_air:
                for serial in my_serials_on_air:
                    tv = serial_info(serial.serial_id)
                    text = "<b>{} ({})</b>\n".format(tv['name'], tv['first_air_date'][:4])
                    text_message += text
                    if tv.get('next_overview'):
                        text = "<i>Episode: {} {}</i>\n{}\n\n".format(tv['next_episode_number'],
                                                             tv['next_name'],
                                                             tv['next_overview'])
                        text_message += text
                    else:
                        text_message += 'Data currently unavailable\n\n'
            else:
                text_message = 'None of your serials are on air today'
            bot.send_message(message.chat.id, text_message, parse_mode='HTML')


def start_bot():
    bot.polling(none_stop=True)
