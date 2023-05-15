import json
from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from . import utils


def main(request):
    return render(request, 'newsapp/index.html',
                  context={'title': 'News',
                           'exchange_rate': utils.exchange_rate(),
                           'weather': utils.weather_current(),
                           'news': utils.unian_news(),
                           }
                  )
