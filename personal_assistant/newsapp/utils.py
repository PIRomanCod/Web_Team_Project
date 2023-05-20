"""This module contains functions for getting news, exchange rate and weather."""

from pathlib import Path

from bs4 import BeautifulSoup
import environ
import requests

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

key_api = env('OPENWEATHER_API_KEY')


def unian_news():
    """
    The unian_news function returns a list of dictionaries, each dictionary containing the header and url for
    the top 10 news articles on unian.ua

    :return: A list of dictionaries
    """
    url = 'https://www.unian.ua/detail/all_news'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    results = soup.find_all('a', {'class': 'list-thumbs__title'})
    return_result = []
    for item in results:
        return_result.append({'header': item.text.replace('\n', ''), 'url': item['href']})
    return return_result[:10]


def exchange_rate():
    """
    The exchange_rate function returns the current exchange rate of USD and EUR to UAH.
    The function uses the PrivatBank API to get a JSON response with all available currencies,
    then it parses this response and returns only two values: USD and EUR.

    :return: A list of dictionaries
    """
    response = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11')
    exch_rate = response.json()
    return exch_rate


def weather_current(city='Kyiv'):
    """
    The weather_current function returns a dictionary with the current weather in Kyiv.
    The dictionary contains three keys: name, icon_url and temp.
    name - city name;
    icon_url - url to the image of the current weather;
    temp - temperature in Celsius degrees.

    :return: The current weather in the city
    """
    city_index = f'{city},ua'
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_index}&appid={key_api}')
    res = response.json()
    weather = {'name': res.get('name'),
               'icon_url': f"https://openweathermap.org/img/wn/{res.get('weather')[0].get('icon')}@2x.png",
               'temp': str('%+d' % (int(res.get('main').get('temp'))-273)) + 'ºC'
               }
    return weather


if __name__ == '__main__':
    print(unian_news())
    print(exchange_rate())
    print(weather_current())
