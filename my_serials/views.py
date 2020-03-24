import tmdbsimple as tmdb

from configparser import ConfigParser

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from . import forms
from . import models


# config = ConfigParser()
# config.read('my_serials/config.cfg')
# tmdb.API_KEY = config['tmdb']['API_KEY']
tmdb.API_KEY = '71af347ad6265c67d36f595aa27ea28c'


def serial_info(serial_id):
    tv = tmdb.TV(serial_id).info()
    info = {'info': tv,
            'name': tv['name'],
            'poster_path': tv['poster_path'],
            'in_production': tv['in_production'],
            'seasons': tv['seasons'],
            'created_by': tv['created_by'],
            }
    if tv['first_air_date']:
        info['first_air_date'] = tv['first_air_date']
    else:
        info['first_air_date'] = 'N/A'
    if tv['last_episode_to_air']:
        info['last_season_number'] = tv['last_episode_to_air']['season_number']
        info['last_episode_number'] = tv['last_episode_to_air']['episode_number']
        info['last_date'] = tv['last_episode_to_air']['air_date']
        info['last_name'] = tv['last_episode_to_air']['name']
        info['last_overview'] = tv['last_episode_to_air']['overview']
    if tv['next_episode_to_air']:
        info['next_season_number'] = tv['next_episode_to_air']['season_number']
        info['next_episode_number'] = tv['next_episode_to_air']['episode_number']
        info['next_date'] = tv['next_episode_to_air']['air_date']
        info['next_name'] = tv['next_episode_to_air']['name']
        info['next_overview'] = tv['next_episode_to_air']['overview']
    return info


def serial_credits(serial_id):
    tv = tmdb.TV(serial_id).credits()
    credits_list = {'cast': tv['cast'],
                    'crew': tv['crew'],
                    }
    return credits_list


def user_serials(some_user):
    return models.Serial.objects.filter(owner=some_user)


def user_serials_check(some_user, serial_id):
    serial_list = user_serials(some_user)
    if serial_id in [serial.serial_id for serial in serial_list]:
        response = True
    else:
        response = False
    return response


def add_serial(request):
    if request.method == 'POST':
        serial_list = user_serials(request.user)
        id_list = [int(s.serial_id) for s in serial_list]
        new_serial = models.Serial()
        new_serial.serial_id = request.POST.get('serial_id')
        if int(new_serial.serial_id) not in id_list:
            tv = serial_info(new_serial.serial_id)
            new_serial.title = tv['name']
            new_serial.air_date = tv['first_air_date'][:4]
            new_serial.owner = request.user
            new_serial.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def delete(request, serial_id):
    try:
        serial = models.Serial.objects.get(id=serial_id)
        serial.delete()
    except ObjectDoesNotExist:
        pass
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def my_serials_list(request):
    serial_list = user_serials(request.user).order_by('title')
    serials = []
    for serial in serial_list:
        result = {'title': serial.title,
                  'id': serial.id,
                  'serial_id': serial.serial_id,
                  'air_date': serial.air_date,
                  }
        result.update(serial_info(serial.serial_id))
        serials.append(result)
    result = {'serials': serials}
    return render(request, 'serial/list.html', result)


@login_required
def search(request):
    query = str(request.GET.get('query', ''))
    if query != '':
        response = tmdb.Search().tv(query=query)['results']
        search_result = [tv for tv in response if tv['poster_path']]
        for elem in search_result:
            serial = serial_info(elem['id'])
            elem['in_production'] = serial['in_production']
            elem['year'] = serial['first_air_date'][:4]
            elem['in_list'] = user_serials_check(request.user, elem['id'])
        result = {'search_result': search_result}
    else:
        result = {'search_result': []}
    return render(request, 'serial/search.html', result)


@login_required
def details(request, db_id):
    tv = serial_info(db_id)
    credits_list = serial_credits(db_id)
    try:
        serial_id = models.Serial.objects.get(owner=request.user,
                                              serial_id=db_id).id
    except ObjectDoesNotExist:
        serial_id = None
    seasons = tv['seasons']
    for season in seasons:
        tv_s = tmdb.TV_Seasons(db_id,
                               season['season_number']).info()['episodes']
        season['episodes'] = tv_s
    result = {
        'serial_id': serial_id,
        'seasons': seasons,
        'info': tv['info'],
        'year': tv['first_air_date'][:4],
        'cast': credits_list['cast'][:15],
        'created_by': tv['created_by'],
    }
    return render(request, "serial/details.html", result)


@login_required
def popular(request):
    popular_list = tmdb.TV().popular()['results']
    for elem in popular_list:
        tv = serial_info(elem['id'])
        elem['in_production'] = tv['in_production']
        elem['year'] = tv['first_air_date'][:4]
        elem['in_list'] = user_serials_check(request.user, elem['id'])
    result = {'popular_list': popular_list}
    return render(request, 'serial/popular.html', result)


@login_required
def on_air_today(request):
    air_today_list = tmdb.TV().airing_today()['results']
    for elem in air_today_list:
        tv = serial_info(elem['id'])
        elem['in_production'] = tv['in_production']
        elem['year'] = tv['first_air_date'][:4]
        elem['in_list'] = user_serials_check(request.user, elem['id'])
    result = {'air_today_list': air_today_list}
    return render(request, 'serial/on_air_today.html', result)


def register(request):
    if request.method == 'POST':
        user_form = forms.UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'],
            )
            new_user.save()
            return render(request, 'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = forms.UserRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {'form': user_form})


@login_required
@transaction.atomic
def edit_profile(request):
    if request.method == 'POST':
        user_form = forms.UserEditForm(instance=request.user,
                                       data=request.POST)
        profile_form = forms.ProfileEditForm(instance=request.user.profile,
                                             data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/home')
        else:
            messages.error(request, 'Please correct the error.')
    else:
        user_form = forms.UserEditForm(instance=request.user)
        profile_form = forms.ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'registration/profile.html',
                  {'user_form': user_form,
                   'profile_form': profile_form}
                  )
