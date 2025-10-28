from django.urls import path
from django.contrib.auth.views import (LogoutView,
                                       PasswordChangeView,
                                       LoginView,
                                       PasswordResetView,
                                       PasswordChangeDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)

from . import views


app_name = 'users'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/',
         LoginView.as_view(
             template_name='users/login.html'),
         name='login'),
    path('signup/',
         views.SighUp.as_view(), name='signup'),
    path('logout/',
         LogoutView.as_view(
             template_name='users/logged_out.html'),
         name='logout'),
    path('password_change/',
         PasswordChangeView.as_view(
             template_name='users/password_change_form.html'),
         name='password_change_form'),
    path('password_reset/',
         PasswordResetView.as_view(
             template_name='users/password_reset_form.html'),
         name='password_reset_form'),
    path('password_reset/done/',
         PasswordChangeDoneView.as_view(
             template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
         name='passwrod_reset_complete'),
]