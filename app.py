from flask import Flask, render_template
from gismeteo import get_gis

from yandex_api import parse_weather
from scraper import get_bs

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    get_gis()
    parse_weather()
    get_bs()

    app.run()
