import requests
from bs4 import BeautifulSoup


def get_bs():
    url = 'https://rp5.ru/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%9F%D0%B5%D1%80%D0%BC%D0%B8'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for row in soup.find_all("div", id="forecastTable_1_3"):

        print(row)
