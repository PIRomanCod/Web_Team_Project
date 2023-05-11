import json
from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


def main(request):
    return render(request, 'newsapp/index.html', context={'title': 'News'})
