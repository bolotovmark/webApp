import requests
from bs4 import BeautifulSoup
import re


def get_bs():
    # onmouseover="tooltip(this, 'Cлабый снег (0.1 см снега за 1 час с 12:00 до 13:00)'
    # <b>-1</b>
    # style="">4<
    url = 'https://rp5.ru/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%9F%D0%B5%D1%80%D0%BC%D0%B8'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', id="forecastTable")
    td = table.find_all('tr')[5]
    b = td.find_all('b')
    for i in range(0, 8):
        if i % 2 == 0:
            print(re.findall(r'(?<!\d)-?\d*[.,]?\d+', str(b[i]))) #t+
