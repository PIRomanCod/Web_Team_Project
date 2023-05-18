"""
In this module, the main page of the application is generated.
"""
import json
from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from . import utils


def main(request):
    """
    The main function is the main page of the site.
    It displays exchange rate, weather and news from unian.net

    :param request: Pass the http request that triggered the view
    :return: The value of the render function
    :doc-author: Trelent
    """
    return render(request, 'newsapp/index.html',
                  context={'title': 'News',
                           'exchange_rate': utils.exchange_rate(),
                           'weather': utils.weather_current(),
                           'news': utils.unian_news(),
                           }
                  )
