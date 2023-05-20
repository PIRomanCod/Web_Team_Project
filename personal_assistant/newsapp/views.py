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
    form = CityForm(request.POST or None)
    if form.is_valid():
        city = form.cleaned_data['city_choice']
        weather = utils.weather_current(city)
        context = {
            'title': 'News',
            'form': form,
            'weather': weather,
            'exchange_rate': utils.exchange_rate(),
            'news': utils.unian_news()
        }
    else:
        context = {'title': 'News',
                   'form': form,
                   'exchange_rate': utils.exchange_rate(),
                   'news': utils.unian_news(),
                   'default_weather': default_weather
                   }
    return render(request, 'newsapp/index.html', context=context)
