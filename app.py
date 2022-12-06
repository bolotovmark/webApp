import os
from flask import Flask, render_template
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup
from datetime import timedelta, datetime

#from parse.archive_parse import get_archive
from parse.gismeteo import get_gis
from parse.yandex_api import parse_weather
from parse.rp5 import get_bs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c8bd55466f90a32a8e90b3e4d6c030cc'

app.config['SCHEDULER_API_ENABLE'] = 'True'
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Archive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, unique=True)
    character = db.Column(db.String(200))
    temp_a = db.Column(db.Integer)
    temp_b = db.Column(db.Integer)
    wind_speed = db.Column(db.Integer)

    def __init__(self, date, character, temp_a, temp_b, wind_speed):
        self.date = date
        self.character = character
        self.temp_a = temp_a
        self.temp_b = temp_b
        self.wind_speed = wind_speed

    def __repr__(self):
        return '<Character %r>' % self.character


class Rp5(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, unique=True)
    character = db.Column(db.String(200))
    temp_a = db.Column(db.Integer)
    temp_b = db.Column(db.Integer)
    wind_speed = db.Column(db.Integer)

    def __init__(self, date, character, temp_a, temp_b, wind_speed):
        self.date = date
        self.character = character
        self.temp_a = temp_a
        self.temp_b = temp_b
        self.wind_speed = wind_speed

    def __repr__(self):
        return '<Character %r>' % self.character


class Gismeteo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, unique=True)
    character = db.Column(db.String(200))
    temp_a = db.Column(db.Integer)
    temp_b = db.Column(db.Integer)
    wind_speed = db.Column(db.Integer)

    def __init__(self, date, character, temp_a, temp_b, wind_speed):
        self.date = date
        self.character = character
        self.temp_a = temp_a
        self.temp_b = temp_b
        self.wind_speed = wind_speed

    def __repr__(self):
        return '<Character %r>' % self.character


class Yandex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, unique=True)
    character = db.Column(db.String(200))
    temp_a = db.Column(db.Integer)
    temp_b = db.Column(db.Integer)
    wind_speed = db.Column(db.Integer)

    def __init__(self, date, character, temp_a, temp_b, wind_speed):
        self.date = date
        self.character = character
        self.temp_a = temp_a
        self.temp_b = temp_b
        self.wind_speed = wind_speed

    def __repr__(self):
        return '<Character %r>' % self.character


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@scheduler.task('cron', id='do_job_1', minute=4, hour=19)
def scheduled_task():
    with app.app_context():
        get_parse()



def get_parse():
    time = datetime.now() - timedelta(days=1)

    print(time)
    url = 'http://www.pogodaiklimat.ru/weather.php?id=28224&bday=' + str(time.day) \
          + '&fday=' + str(time.day) + '&amonth=' + str(time.month) + \
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
        print(i, j)
        td = tr[i].find_all('td')
        print(td[1].text)
        print(td[3].text)
        print(td[5].text)
        print('--------------')

        time = time.replace(hour=j)
        event = Archive(date=time, character=td[3].text,
                        temp_a=td[5].text, temp_b=td[5].text, wind_speed=td[1].text)
        db.session.add(event)
        db.session.commit()


if __name__ == '__main__':
    app.run()
