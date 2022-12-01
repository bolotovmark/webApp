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
    td = table.find_all('tr')

    temper = td[5]
    b = temper.find_all('b')
    for i in range(0, 8):
        if i % 2 == 0:
            m = re.search(r'(?<!\d)-?\d*[.,]?\d+', str(b[i]))
            print(m.group(0))  # t + - 0

    wind = td[8]
    for i in range(1, 5):
        wind_temp = wind.find_all('td')[i]
        dive = wind_temp.find_all('div')[0]
        print(dive.string)

    precipitation = td[3]
    for i in range(1, 5):
        prec_temp = precipitation.find_all('td')[i]
        dive = prec_temp.find_all('div')[0]
        onmouseover = BeautifulSoup(str(dive), 'html.parser')
        text = str(onmouseover.div['onmouseover'])
        print(text)
        print(re.match(r"(?<=')[\w\s]+", text))
