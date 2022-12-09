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
    print(temper)
    b = temper.find_all('b')
    for i in [8, 10, 12, 14]:
        m = re.search(r'(?<!\d)-?\d*[.,]?\d+', str(b[i]))
        print(m.group(0))  # t + - 0


    wind = td[8]
    for i in range(5, 9):
        wind_temp = wind.find_all('td')[i]
        try:
            dive = wind_temp.find_all('div')[0]
        except Exception:
            dive = wind_temp
        print(dive.contents[0])

    precipitation = td[2]
    cloudy = td[3]
    for i in range(5, 9):
        prec_temp = precipitation.find_all('td')[i]
        dive = prec_temp.find_all('div')[1]
        onmouseover = BeautifulSoup(str(dive), 'html.parser')
        text = onmouseover.div['onmouseover']
        m1 = re.search(r"(?<=>)[\w\s]+", text)

        cloudy_temp = cloudy.find_all('td')[i]
        dive = cloudy_temp.find_all('div')[0]
        onmouseover = BeautifulSoup(str(dive), 'html.parser')

        dive_onmouseover = onmouseover.find_all('div')[0]
        text = str(dive_onmouseover['onmouseover'])
        m2 = re.search(r"(?<=')[\w\s]+", text)
        out = m2.group(0) + " " + m1.group(0)
        print(out)



