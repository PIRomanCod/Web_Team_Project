"""
This module is used to define the urls for the newsapp.

"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='root'),
]
