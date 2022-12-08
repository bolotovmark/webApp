import os
import re
import requests
from datetime import timedelta, datetime
from bs4 import BeautifulSoup
from flask import Flask, render_template
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

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


@scheduler.task('cron', id='do_job_1', minute=14, hour=2)
def scheduled_task():
    with app.app_context():
        get_parse()
        rp5()


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
    for i, j in zip([-7, -5, -3, -1], [5, 11, 17, 23]):
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


def rp5():
    # onmouseover="tooltip(this, 'Cлабый снег (0.1 см снега за 1 час с 12:00 до 13:00)'
    # <b>-1</b>
    # style="">4<
    url = 'https://rp5.ru/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%9F%D0%B5%D1%80%D0%BC%D0%B8'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', id="forecastTable")
    td = table.find_all('tr')

    for i, j, k in zip([5, 6, 7, 8], [8, 10, 12, 14], [5, 11, 17, 23]):
        temper = td[5]

        b = temper.find_all('b')
        m = re.search(r'(?<!\d)-?\d*[.,]?\d+', str(b[j]))
        temp_a_out = m.group(0)
        temp_b_out = m.group(0)  # t + - 0

        wind = td[8]
        wind_temp = wind.find_all('td')[i]
        try:
            dive = wind_temp.find_all('div')[0]
        except Exception:
            dive = wind_temp
        wind_out = dive.contents[0]

        precipitation = td[2]
        cloudy = td[3]

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
        character_out = m2.group(0) + " " + m1.group(0)

        time = datetime.now()
        time = time.replace(hour=k)
        event = Rp5(date=time, character=character_out,
                    temp_a=temp_a_out, temp_b=temp_b_out, wind_speed=wind_out)
        db.session.add(event)
        db.session.commit()


if __name__ == '__main__':
    app.run()
