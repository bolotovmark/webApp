import requests, json


def parse_weather():
    # утро - 5:00 день - 11 вечер 17 ночь 23
    # характер погоды : осадки и облачки
    # температура + - 0
    # ветер м/c
    url = 'https://api.weather.yandex.ru/v2/forecast?lat=55.75396&lon=37.620393&lang=ru_RU&limit=1&hours=true&extra=true'
    response = requests.get(url, headers={'X-Yandex-API-Key': '25953e0d-5412-41e2-885a-0db6e929f689'})
    print(response.json())

