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

    weather = soup.find_all("div", class_="widget-row widget-row-icon")[0]
    weather_out = []
    for i, j in zip(range(0, 8), weather):
        if i % 2 == 1:
            row_w = j.find('div')
            data = BeautifulSoup(str(row_w), 'html.parser')
            text = str(data.div['data-text'])
            weather_out.append(text)

    t = soup.find_all("div", class_="widget-row-chart widget-row-chart-temperature")[0]
    temp = t.find_all("span", class_="unit unit_temperature_c")
    temp_out = []
    for i, j in zip(range(0, 8), temp):
        if i % 2 == 1:
            temp_out.append(j.contents[0])

    s = soup.find_all("div", class_="widget-row widget-row-wind-speed-gust row-with-caption")[0]
    speed_a_out = []
    speed_b_out = []
    for i, j in zip(range(0, 10), s):
        if i % 2 == 0 and i != 0:
            speed = j.find_all("span")
            output = str(speed[0].contents[0])
            if len(output) > 2:
                m = re.findall(r'(?<!\d)-?\d*[.,]?\d+', output)
                speed_a_out.append(m[0])
                speed_b_out.append(m[1])
            else:
                speed_a_out.append(output)
                speed_b_out.append(output)

    for i, j, k, h in zip(weather_out, temp_out, speed_a_out, speed_b_out):
        print(i)
        print(j)
        print(k)
        print(h)
        print("-------------")
