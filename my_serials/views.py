from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from . import models
from django.contrib.auth.models import User
from django.views.generic import ListView

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from . import forms

import re

import tmdbsimple as tmdb
tmdb.API_KEY = '71af347ad6265c67d36f595aa27ea28c'

# Create your views here.


def all_serials(request):
    serial_list = models.Serial.objects.all()
    return render(request,
                  'serial/list.html',
                  {"serials": serial_list})


def serial_details(request, serial_id, slug):
    serial = get_object_or_404(models.Serial, serial_id=serial_id, slug=slug)
    return render(request,
                  'serial/detail.html',
                  {'serial': serial})


def search_form(request):
    query = str(request.GET.get('query', ''))
    if query != '':
        search_result = tmdb.Search().tv(query=query)['results']
        result = {'search_result': search_result, 'has_result': True}
    else:
        result = {'search_result': [], 'has_result': False}
    return render(request, 'serial/search.html', result)


def details(request, id=None):
    serial = tmdb.TV(id)
    # trailers = list(filter(lambda v: v['type'] == 'Trailer', serial.videos()['results']))
    # teasers = list(filter(lambda v: v['type'] == 'Teaser', serial.videos()['results']))
    # keywords = movie.keywords()['keywords']
    from pprint import pprint
    # pprint(movie.reviews()['results'])
    frontend = {
        "info": serial.info(),
        # "year": serial.info()['first_air_date'][:4],
        # "cast": movie.credits()['cast'][:15],
        # "crew": movie.credits()['crew'][:15],
        # "trailers": trailers,
        # "teasers": teasers,
        # "keywords": keywords,
        # "reviews": movie.reviews()['results'],
        # "alt": movie.alternative_titles()['titles']
    }
    return render(request, "serial/details.html", frontend)


def add_form(request):
    if request.method == 'POST':
        serial_form = forms.SerialForm(request.POST)
        if serial_form.is_valid():
            cd = serial_form.cleaned_data
            db_id = cd['serial_id']
            new_serial = serial_form.save(commit=False)
            serial_db = tmdb.TV(db_id)
            response = serial_db.info()
            title = response['name']
            air_date = response['first_air_date'][0:4]
            new_serial.poster_path = response['poster_path']
            new_serial.title = title.replace("'", "")
            new_serial.air_date = air_date
            new_serial.slug = new_serial.title.replace(" ", "-")
            new_serial.save()
            return render(request,
                          'serial/detail.html',
                          {'serial': new_serial})
    else:
        serial_form = forms.SerialForm()
    return render(request, "serial/add_serial.html", {'form': serial_form})
