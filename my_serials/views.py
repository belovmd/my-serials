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

# Create your views here.


@login_required
def all_serials(request):
    serial_list = models.Serial.objects.all()
    user_serial_list = [serial for serial in serial_list if serial.owner == request.user]
    result = {"serials": user_serial_list}
    return render(request, 'serial/list.html', result)


def search_form(request):
    query = str(request.GET.get('query', ''))
    if query != '':
        search_result = tmdb.Search().tv(query=query)['results']
        result = {'search_result': search_result, 'has_result': True}
    else:
        result = {'search_result': [], 'has_result': False}
    return render(request, 'serial/search.html', result)


def details(request, db_id=None):
    tv = tmdb.TV(db_id)
    # trailers = list(filter(lambda v: v['type'] == 'Trailer', serial.videos()['results']))
    # teasers = list(filter(lambda v: v['type'] == 'Teaser', serial.videos()['results']))
    # keywords = movie.keywords()['keywords']
    from pprint import pprint
    # pprint(movie.reviews()['results'])
    result = {
        "info": tv.info(),
        "year": tv.info()['first_air_date'][:4],
        # "cast": movie.credits()['cast'][:15],
        # "crew": movie.credits()['crew'][:15],
        # "trailers": trailers,
        # "teasers": teasers,
        # "keywords": keywords,
        # "reviews": movie.reviews()['results'],
        # "alt": movie.alternative_titles()['titles']
    }
    return render(request, "serial/details.html", result)


# def add_form(request):
#     if request.method == 'POST':
#         serial_form = forms.SerialForm(request.POST)
#         if serial_form.is_valid():
#             cd = serial_form.cleaned_data
#             db_id = cd['serial_id']
#             new_serial = serial_form.save(commit=False)
#             serial_db = tmdb.TV(db_id)
#             response = serial_db.info()
#
#             new_serial.poster_path = response['poster_path']
#             new_serial.title = response['name']
#             new_serial.air_date = response['first_air_date'][0:4]
#             new_serial.save()
#
#             return render(request,
#                           'serial/list.html',
#                           {'serial': new_serial})
#     else:
#         serial_form = forms.SerialForm()
#     return render(request, "serial/add_serial.html", {'form': serial_form})


def add_serial(request):
    if request.method == 'POST':
        new_serial = models.Serial()
        new_serial.serial_id = request.POST.get('serial_id')
        serial_id_list = [s.serial_id for s in models.Serial.objects.all() if s.owner == request.user]
        if int(new_serial.serial_id) not in serial_id_list:
            response = tmdb.TV(request.POST.get('serial_id')).info()
            if response['in_production']:
                new_serial.title = response['name']
                new_serial.poster_path = response['poster_path']
                new_serial.air_date = response['first_air_date'][0:4]
                new_serial.owner = request.user
                new_serial.save()
            else:
                return HttpResponse('Sorry, show is canceled')
        else:
            return HttpResponse('Already in your list')
    return HttpResponseRedirect('/')


def delete(request, id):
    serial = models.Serial.objects.get(id=id)
    serial.delete()
    return HttpResponseRedirect("/")
