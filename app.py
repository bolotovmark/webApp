from flask import Flask, render_template
from yandex_api import parse_weather

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    parse_weather()
    app.run()
