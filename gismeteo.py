from bs4 import BeautifulSoup
import requests
import re


def get_gis():
    # onmouseover="tooltip(this, 'Cлабый снег (0.1 см снега за 1 час с 12:00 до 13:00)'
    # <b>-1</b>
    # style="">4<
    url = 'https://www.gismeteo.ru/weather-perm-4476/tomorrow'
    headers = requests.utils.default_headers()

    headers.update(
        {
            'User-Agent': 'My User Agent 1.0',
        }
    )

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find_all('div', class_="widget-row widget-row-icon")
    print(table)
