from flask import Flask, render_template

from parse.archive_parse import get_archive
from parse.gismeteo import get_gis
from parse.yandex_api import parse_weather
from parse.rp5 import get_bs

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    get_archive()
    get_gis()
    parse_weather()
    get_bs()

    app.run()
