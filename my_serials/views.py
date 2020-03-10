from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from . import models
from django.contrib.auth.decorators import login_required
from . import forms

from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

import tmdbsimple as tmdb
tmdb.API_KEY = '71af347ad6265c67d36f595aa27ea28c'


@login_required
def all_serials(request):
    serial_list = models.Serial.objects.filter(owner=request.user).order_by('title')
    result = {"serials": serial_list}
    return render(request, 'serial/list.html', result)


@login_required
def search_form(request):
    serial_list = models.Serial.objects.filter(owner=request.user)
    query = str(request.GET.get('query', ''))
    if query != '':
        search_result = tmdb.Search().tv(query=query)['results']
        for elem in search_result:
            elem['in_production'] = tmdb.TV(elem['id']).info()['in_production']
            elem['first_air_date'] = elem.get('first_air_date', 'N/A')[:4]
            if elem['id'] in [s.serial_id for s in serial_list]:
                elem['in_list'] = True
            else:
                elem['in_list'] = False
        result = {'search_result': search_result}
    else:
        result = {'search_result': []}
    return render(request, 'serial/search.html', result)


@login_required
def details(request, db_id=None):
    tv = tmdb.TV(db_id)
    # trailers = list(filter(lambda v: v['type'] == 'Trailer', serial.videos()['results']))
    # teasers = list(filter(lambda v: v['type'] == 'Teaser', serial.videos()['results']))
    # keywords = movie.keywords()['keywords']
    from pprint import pprint
    # pprint(movie.reviews()['results'])
    result = {
        'info': tv.info(),
        'year': tv.info()['first_air_date'][:4],
        'in_production': tv.info()['in_production'],

        # "cast": movie.credits()['cast'][:15],
        # "crew": movie.credits()['crew'][:15],
        # "trailers": trailers,
        # "teasers": teasers,
        # "keywords": keywords,
        # "reviews": movie.reviews()['results'],
        # "alt": movie.alternative_titles()['titles']
    }
    return render(request, "serial/details.html", result)


def add_serial(request):
    if request.method == 'POST':
        new_serial = models.Serial()
        new_serial.serial_id = request.POST.get('serial_id')
        response = tmdb.TV(request.POST.get('serial_id')).info()
        new_serial.title = response['name']
        new_serial.poster_path = response['poster_path']
        if response['first_air_date']:
            new_serial.air_date = response['first_air_date'][:4]
        new_serial.owner = request.user
        new_serial.save()
    return HttpResponseRedirect('/')


def delete(request, id):
    serial = models.Serial.objects.get(id=id)
    serial.delete()
    return HttpResponseRedirect("/")
