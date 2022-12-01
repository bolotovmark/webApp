import requests
from bs4 import BeautifulSoup
import re

def get_archive():
    url = 'http://www.pogodaiklimat.ru/weather.php?id=28224'
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
    for i in {-7, -5, -3, -1}:
        #print(tr[i], "\n--------------\n")
        td = tr[i].find_all('td')
        print(td[1].text)
        print(td[3].text)
        print(td[5].text)



