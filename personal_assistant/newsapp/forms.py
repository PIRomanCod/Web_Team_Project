from django import forms
import configparser
from pathlib import Path

file_config = Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

CITIES = config.get('DEV', 'cities').split(' ')


class CityForm(forms.Form):
    city_choice = forms.ChoiceField(choices=[(city, city) for city in CITIES])
