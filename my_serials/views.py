from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from . import models
from django.contrib.auth.decorators import login_required
from . import forms
from django.core.exceptions import ObjectDoesNotExist

from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

import tmdbsimple as tmdb
tmdb.API_KEY = '71af347ad6265c67d36f595aa27ea28c'


def add_serial(request):
    if request.method == 'POST':
        serial_list = models.Serial.objects.filter(owner=request.user)
        id_list = [int(s.serial_id) for s in serial_list]
        new_serial = models.Serial()
        new_serial.serial_id = request.POST.get('serial_id')
        if int(new_serial.serial_id) not in id_list:
            response = tmdb.TV(new_serial.serial_id).info()
            new_serial.title = response['name']
            # new_serial.poster_path = response['poster_path']
            if response['first_air_date']:
                new_serial.air_date = response['first_air_date'][:4]
            new_serial.owner = request.user
            new_serial.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def delete(request, id):
    try:
        serial = models.Serial.objects.get(id=id)
        serial.delete()
    except ObjectDoesNotExist:
        pass
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def all_serials(request):
    serial_list = models.Serial.objects.filter(owner=request.user).order_by('title')
    result = {'serials': serial_list}
    return render(request, 'serial/list.html', result)


@login_required
def popular(request):
    serial_list = models.Serial.objects.filter(owner=request.user)
    popular_list = tmdb.TV().popular()['results']
    for elem in popular_list:
        elem['in_production'] = tmdb.TV(elem['id']).info()['in_production']
        elem['year'] = elem.get('first_air_date')
        if elem['year']:
            elem['year'] = elem['year'][:4]
        else:
            elem['year'] = 'N/A'
        if elem['id'] in [s.serial_id for s in serial_list]:
            elem['in_list'] = True
        else:
            elem['in_list'] = False
    result = {'popular_list': popular_list}
    return render(request, 'serial/popular.html', result)


@login_required
def on_air_today(request):
    serial_list = models.Serial.objects.filter(owner=request.user)
    air_today_list = tmdb.TV().airing_today()['results']
    for elem in air_today_list:
        elem['year'] = elem.get('first_air_date')
        if elem['year']:
            elem['year'] = elem['year'][:4]
        else:
            elem['year'] = 'N/A'
        if elem['id'] in [s.serial_id for s in serial_list]:
            elem['in_list'] = True
        else:
            elem['in_list'] = False
    result = {'air_today_list': air_today_list}
    return render(request, 'serial/on_air_today.html', result)


@login_required
def search(request):
    serial_list = models.Serial.objects.filter(owner=request.user)
    query = str(request.GET.get('query', ''))
    if query != '':
        response = tmdb.Search().tv(query=query)['results']
        search_result = [serial for serial in response if serial['poster_path']]
        for elem in search_result:
            elem['in_production'] = tmdb.TV(elem['id']).info()['in_production']
            elem['year'] = elem.get('first_air_date')
            if elem['year']:
                elem['year'] = elem['year'][:4]
            else:
                elem['year'] = 'N/A'

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
    serial = list(models.Serial.objects.
                  filter(owner=request.user, serial_id=db_id).values('id'))
    if serial:
        serial_id = serial[0]['id']
    else:
        serial_id = None
    year = tv.info().get('first_air_date')
    if year:
        year = year[:4]
    else:
        year = 'N/A'
    seasons = tv.info()['seasons']
    for season in seasons:
        tv_s = tmdb.TV_Seasons(db_id, season['season_number']).info()['episodes']
        season['episodes'] = tv_s
    result = {
        # 'serial': serial,
        'serial_id': serial_id,
        'seasons': seasons,
        'info': tv.info(),
        'year': year,
        'cast': tv.credits()['cast'][:15],
        'created_by': tv.info()['created_by'],
    }
    return render(request, "serial/details.html", result)


def register(request):
    if request.method == 'POST':
        user_form = forms.UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'],
            )
            new_user.save()
            # models.Profile.objects.create(user=new_user,
            #                               photo='unknown.jpeg')
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = forms.UserRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {'form': user_form})

