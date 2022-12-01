import requests, json


def parse_weather():
    # утро - 5:00  'morning' день - 11 'day' вечер 17 'evening' ночь 23 'night'
    # характер погоды : осадки и облачки 'condition' 'cloudness'
    # температура + - 0 'temp_avg'
    # ветер м/c 'wind_speed'
    url = 'https://api.weather.yandex.ru/v2/forecast?lat=58.010000&lon=56.229143&lang=ru_RU&limit=2&hours=true&extra=true'
    response = requests.get(url, headers={'X-Yandex-API-Key': '25953e0d-5412-41e2-885a-0db6e929f689'}).json()
    count = 1
    for part in response['forecasts']:
        if count == 1:
            count = 2
        else:
            day_condition = part['parts']['day']['condition']
            day_cloudness = part['parts']['day']['cloudness']
            day_temp = part['parts']['day']['temp_avg']
            day_wind = part['parts']['day']['wind_speed']
            #
            night_condition = part['parts']['night']['condition']
            night_cloudness = part['parts']['night']['cloudness']
            night_temp = part['parts']['night']['temp_avg']
            night_wind = part['parts']['night']['wind_speed']
            #
            morning_condition = part['parts']['morning']['condition']
            morning_cloudness = part['parts']['morning']['cloudness']
            morning_temp = part['parts']['morning']['temp_avg']
            morning_wind = part['parts']['morning']['wind_speed']
            #
            evening_condition = part['parts']['evening']['condition']
            evening_cloudness = part['parts']['evening']['cloudness']
            evening_temp = part['parts']['evening']['temp_avg']
            evening_wind = part['parts']['evening']['wind_speed']

            mas_weather = [[morning_condition, morning_cloudness, morning_temp, morning_wind],[day_condition, day_cloudness, day_temp, day_wind],[evening_condition, evening_cloudness, evening_temp, evening_wind],[night_condition, night_cloudness, night_temp, night_wind]]
            for row in mas_weather:
                for elem in row:
                    print(elem, end=' ')
                print()



