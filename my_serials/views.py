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


# Create your views here.


def all_serials(request):
    serial_list = models.Serial.objects.all()
    return render(request,
                  'serial/list.html',
                  {"serials": serial_list})


def create_form(request):
    if request.method == 'POST':
        serial_form = forms.SerialForm(request.POST)
        if serial_form.is_valid():
            new_serial = serial_form.save(commit=False)
            new_serial.save()
            return render(request,
                          'serial/detail.html',
                          {'serial': new_serial})
    else:
        serial_form = forms.SerialForm()
    return render(request, "serial/add_serial.html", {'form': serial_form})
