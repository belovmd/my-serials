from django.urls import path
from . import views

app_name = 'my_serials'


urlpatterns = [
    path('', views.all_serials, name='all_serials'),
    path('add/', views.add_form, name='add_form'),
    path('search/', views.search_form, name='search_form'),
    path('<int:serial_id>-<slug:slug>/', views.serial_details, name='serial_details'),
    path('details/<id>', views.details, name='details'),
]
