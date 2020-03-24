from django.contrib.auth import views as au_views
from django.shortcuts import redirect
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from . import views

app_name = 'my_serials'

urlpatterns = [
    # path('', lambda request: redirect('home/')),
    path('', RedirectView.as_view(url='home/')),
    path('home/', views.my_serials_list, name='my_serials_list'),
    path('search/', views.search, name='search'),
    path('add/', views.add_serial, name='add_serial'),
    path('delete/', views.delete, name='delete'),
    path('delete/<serial_id>/', views.delete, name='delete'),
    path('details/', views.details, name='details'),
    path('details/<db_id>', views.details, name='details'),
    path('popular/', views.popular, name='popular'),
    path('on_air_today/', views.on_air_today, name='on_air_today'),
    # Registration/Profile edit
    path('register/', views.register, name='register'),
    path('profile/', views.edit_profile, name='profile'),
    # Login/Logout
    path('login/', au_views.LoginView.as_view(), name='login'),
    path('logout/', au_views.LogoutView.as_view(), name='logout'),
    # Password change
    path('password_change/', au_views.PasswordChangeView.as_view(
         success_url=reverse_lazy('my_serials:password_change_done')),
         name='password_change'),
    path('password_change/done/', au_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    # Password reset
    path('password_reset/', au_views.PasswordResetView.as_view(
         success_url=reverse_lazy('my_serials:password_reset_done')),
         name='password_reset'),
    path('password_reset/done/', au_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', au_views.PasswordResetConfirmView.as_view(
         success_url=reverse_lazy('my_serials:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/', au_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
