from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login,name='login'),
    path('apikey/', views.apikey,name='apikey'),
    path('logout/', views.logout_view, name='logout'),
]
