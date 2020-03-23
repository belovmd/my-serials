import django
import os
import telebot
import schedule
import time
import tmdbsimple as tmdb

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_django_project.settings")
django.setup()

from my_serials.models import Serial, User, Profile
from my_serials.views import serial_info

bot = telebot.TeleBot('1011249006:AAEEWYV0BqIrRkHkLMt2rT-wztmr5nXRHa0')


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


schedule.every(10).minutes.do(send_notification)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
