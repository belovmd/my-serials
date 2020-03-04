from django.urls import path
from . import views

app_name = 'my_serials'


urlpatterns = [
    path('', views.all_serials, name='all_serials'),
    path('create/', views.create_form, name='create_form'),
]
