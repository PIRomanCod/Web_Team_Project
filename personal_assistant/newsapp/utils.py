import configparser
from pathlib import Path

from bs4 import BeautifulSoup
import environ
import requests

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

file_config = Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

city = config.get('DEV', 'city')

key_api = env('OPENWEATHER_API_KEY')


def unian_news():
    url = 'https://www.unian.ua/detail/all_news'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    results = soup.find_all('a', {'class': 'list-thumbs__title'})
    return_result = []
    for item in results:
        return_result.append({'header': item.text.replace('\n', ''), 'url': item['href']})
    return return_result[:10]


def exchange_rate():
    response = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11')
    exch_rate = response.json()
    return exch_rate


def weather_current():
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
