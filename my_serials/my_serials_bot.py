from configparser import ConfigParser
import tmdbsimple as tmdb
import telebot
import os
import django



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_django_project.settings")
django.setup()


from my_serials.models import Serial, User
from my_serials.views import serial_info

# tmdb.API_KEY = '71af347ad6265c67d36f595aa27ea28c'


# def serial_info(serial_id):
#     tv = tmdb.TV(serial_id).info()
#     info = {'info': tv,
#             'name': tv['name'],
#             'poster_path': tv['poster_path'],
#             'in_production': tv['in_production'],
#             'seasons': tv['seasons'],
#             'created_by': tv['created_by'],
#             }
#     if tv['first_air_date']:
#         info['first_air_date'] = tv['first_air_date']
#     else:
#         info['first_air_date'] = 'N/A'
#     if tv['last_episode_to_air']:
#         info['last_date'] = tv['last_episode_to_air']['air_date']
#         info['last_name'] = tv['last_episode_to_air']['name']
#         info['last_overview'] = tv['last_episode_to_air']['overview']
#     if tv['next_episode_to_air']:
#         info['next_date'] = tv['next_episode_to_air']['air_date']
#         info['next_name'] = tv['next_episode_to_air']['name']
#         info['next_overview'] = tv['next_episode_to_air']['overview']
#     return info


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
        users = User.objects.all().select_related('profile')
        user = None
        for elem in users:
            if elem.profile.telegram_id == message.chat.id:
                user = elem

        if not user:
            bot.send_message(message.chat.id,
                             '<b>You are not connected to data base!</b>\n'
                             'Enter your <i>chat id</i> on edit profile page',
                             parse_mode='HTML')
        else:
            serial_list = Serial.objects.filter(owner=user).order_by('title')
            text_message = '<u>My Serials:</u>\n'
            for elem in serial_list:
                tv = serial_info(elem.serial_id)
                text = "<b>{} ({})</b>\n".format(tv['name'], tv['first_air_date'][:4])
                text_message += text
                if tv.get('next_overview'):
                    text = "<i>{} {}</i>\n{}\n\n".format(tv['next_date'],
                                                         tv['next_name'],
                                                         tv['next_overview'])
                    text_message += text
                else:
                    error_text = 'Data currently unavailable\n\n'
                    text_message += error_text
            bot.send_message(message.chat.id, text_message, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
