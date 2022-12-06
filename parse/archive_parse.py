import requests
from bs4 import BeautifulSoup
import datetime
from app import db, Archive


def get_archive():
    time = datetime.datetime.now()

    url = 'http://www.pogodaiklimat.ru/weather.php?id=28224&bday=' + str(time.day - 1) \
          + '&fday=' + str(time.day - 1) + '&amonth=' + str(time.month) + \
          '&ayear=' + str(time.year) + '&bot=2'
    headers = requests.utils.default_headers()

    headers.update(
        {
            'User-Agent': 'My User Agent 1.0',
        }
    )
    response = requests.get(url)
    response.encoding = "unf-8"
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('div', class_="archive-table-wrap")
    tr = table.findAll('tr')

    for i, j in zip([-8, -6, -4, -2], [5, 11, 18, 23]):
        # print(tr[i], "\n--------------\n")
        td = tr[i].find_all('td')
        print(td[1].text)
        print(td[3].text)
        print(td[5].text)
        print('--------------')

        time.replace(day=(time.day - 1), hour=j)
        event = Archive(date=time, character=td[3].text,
                        temp_a=td[5].text, temp_b=td[5].text, wind_speed=td[1].text)
        db.session.add(event)
        db.session.commit()
