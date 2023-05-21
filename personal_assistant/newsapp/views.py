"""
In this module, the main page of the application is generated.
"""
import json
from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CityForm
from . import utils


def main(request):
    """
    The main function is the main page of the site.
    It displays exchange rate, weather and news from unian.net

    :param request: Pass the http request that triggered the view
    :return: The value of the render function
    """
    default_weather = utils.weather_current('Kyiv')
    result_dou = utils.dou_scrap()
    form_weather = CityForm(request.POST or None)
    if form_weather.is_valid():
        city = form_weather.cleaned_data['city_choice']
        weather = utils.weather_current(city)
        context = {
            'title': 'News',
            'form_weather': form_weather,
            'weather': weather,
            'exchange_rate': utils.exchange_rate(),
            'news': utils.unian_news(),
            'dou': result_dou
        }
    else:
        context = {'title': 'News',
                   'form_weather': form_weather,
                   'exchange_rate': utils.exchange_rate(),
                   'news': utils.unian_news(),
                   'default_weather': default_weather,
                   'dou': result_dou
                   }
    return render(request, 'newsapp/index.html', context=context)
