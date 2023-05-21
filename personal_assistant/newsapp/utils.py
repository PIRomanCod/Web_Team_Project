"""This module contains functions for getting news, exchange rate and weather."""
import configparser
import json
import platform
from datetime import datetime
from pathlib import Path


import environ
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

file_config = Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

LANGUAGE = config.get('DEV', 'language')
GRADE = config.get('DEV', 'grade')

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

key_api = env('OPENWEATHER_API_KEY')

if platform.system() == 'Windows':
    path_driver = BASE_DIR.joinpath('newsapp', 'static', 'newsapp', 'driver_win', 'chromedriver.exe')
elif platform.system() == 'Linux':
    path_driver = BASE_DIR.joinpath('newsapp', 'static', 'newsapp', 'driver_linux', 'chromedriver.exe')
else:
    path_driver = None

service = Service(str(path_driver))
options = webdriver.ChromeOptions()
options.add_argument('--headless=chrome')

path_dou_json = BASE_DIR.joinpath('newsapp', 'templates', 'newsapp', 'dou.json')

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
    return return_result[:12]


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
               'temp': str('%+d' % (int(res.get('main').get('temp')) - 273)) + 'ºC'
               }
    return weather


def scrap_posts(driver):
    driver.get("https://jobs.dou.ua/vacancies/?category=Python")
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(
        (By.XPATH, '/html//div[@class="b-inner-page-header"]/h1'))
    )
    header = driver.find_element(by=By.XPATH, value='/html//div[@class="b-inner-page-header"]/h1')
    return header.text.split(' ')[0]


def scrap_salary(driver, date_salary):
    driver.get(f"https://jobs.dou.ua/salaries/?period={date_salary}&position={GRADE}%20SE&technology={LANGUAGE}")
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(
        (By.XPATH, '/html/body//div[@id="median"]/div/span'))
    )
    return driver.find_element(by=By.XPATH, value='/html/body//div[@id="median"]/div/span[@class="bc-num-value"]').text


def verify_date_salary(scrap_date):
    if scrap_date.month < 3:
        date_salary = f'{scrap_date.year - 1}-06'
    elif scrap_date.month > 7:
        date_salary = f'{scrap_date.year}-06'
    else:
        date_salary = f'{scrap_date.year - 1}-12'
    return date_salary


def dou_scrap():
    if path_driver is None:
        return ''
    scrap_date = datetime.now()
    date_salary = verify_date_salary(scrap_date)

    with open(path_dou_json, 'r') as file:
        load_res = json.load(file)

    salary = load_res['salary']
    posts_volume = load_res['posts']

    if load_res['date_salary'] != date_salary:
        with webdriver.Chrome(service=service, options=options) as driver:
            salary = scrap_salary(driver, date_salary)

    if load_res['date'] != scrap_date.strftime('%Y-%m-%d'):
        with webdriver.Chrome(service=service, options=options) as driver:
            posts_volume = scrap_posts(driver)

    res_json = {'date': scrap_date.strftime('%Y-%m-%d'),
                'posts': posts_volume,
                'date_salary': date_salary,
                'salary': salary,
                'grade': GRADE,
                'language': LANGUAGE}

    if res_json != load_res:
        with open(path_dou_json, 'w') as file:
            json.dump(res_json, file)
    return res_json


def dou_load():
    with open(path_dou_json, 'r') as file:
        load_res = json.load(file)
        return load_res


if __name__ == '__main__':
    # print(unian_news())
    # print(exchange_rate())
    # print(weather_current())
    print(dou_scrap())
