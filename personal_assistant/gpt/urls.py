"""
This module contains all the urls for the gpt app.
"""
from django.urls import path

from gpt.views import chat
from gpt.views import text_correction
from gpt.views import tasks

app_name = 'gpt'

urlpatterns = [
    path('text_correction/', text_correction, name='text_correction'),
    path('chat/', chat, name='chat'),
    path('tasks/', tasks, name='tasks'),
]