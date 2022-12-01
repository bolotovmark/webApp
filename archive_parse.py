import requests
from bs4 import BeautifulSoup
import re

def get_archive():
    url = 'http://www.hmn.ru/index.php?index=8&value=28224'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', class_="m80")
    tr = table.findAll('tr')
    for i in {1, 3, 5, 7}:
        td = tr[i].findAll('td')
        print(tr[i])


