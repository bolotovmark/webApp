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
    wind_speed_a = db.Column(db.Integer)
    wind_speed_b = db.Column(db.Integer)

    def __init__(self, date, character, temp_a, temp_b, wind_speed_a, wind_speed_b):
        self.date = date
        self.character = character
        self.temp_a = temp_a
        self.temp_b = temp_b
        self.wind_speed_a = wind_speed_a
        self.wind_speed_b = wind_speed_b

    def __repr__(self):
        return '<Character %r>' % self.character


class Rp5(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, unique=True)
    character = db.Column(db.String(200))
    temp_a = db.Column(db.Integer)
    temp_b = db.Column(db.Integer)
    wind_speed_a = db.Column(db.Integer)
    wind_speed_b = db.Column(db.Integer)

    def __init__(self, date, character, temp_a, temp_b, wind_speed_a, wind_speed_b):
        self.date = date
        self.character = character
        self.temp_a = temp_a
        self.temp_b = temp_b
        self.wind_speed_a = wind_speed_a
        self.wind_speed_b = wind_speed_b

    def __repr__(self):
        return '<Character %r>' % self.character


class Gismeteo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, unique=True)
    character = db.Column(db.String(200))
    temp_a = db.Column(db.Integer)
    temp_b = db.Column(db.Integer)
    wind_speed_a = db.Column(db.Integer)
    wind_speed_b = db.Column(db.Integer)

    def __init__(self, date, character, temp_a, temp_b, wind_speed_a, wind_speed_b):
        self.date = date
        self.character = character
        self.temp_a = temp_a
        self.temp_b = temp_b
        self.wind_speed_a = wind_speed_a
        self.wind_speed_b = wind_speed_b

    def __repr__(self):
        return '<Character %r>' % self.character


class Yandex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, unique=True)
    character = db.Column(db.String(200))
    temp_a = db.Column(db.Integer)
    temp_b = db.Column(db.Integer)
    wind_speed_a = db.Column(db.Integer)
    wind_speed_b = db.Column(db.Integer)

    def __init__(self, date, character, temp_a, temp_b, wind_speed_a, wind_speed_b):
        self.date = date
        self.character = character
        self.temp_a = temp_a
        self.temp_b = temp_b
        self.wind_speed_a = wind_speed_a
        self.wind_speed_b = wind_speed_b

    def __repr__(self):
        return '<Character %r>' % self.character


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@scheduler.task('cron', id='do_job_1', minute=10, hour=23)
def scheduled_task():
    with app.app_context():
        get_parse()
        rp5()
        gismeteo()
        yandex()


def get_parse():
    time = datetime.now() - timedelta(days=1)

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
        td = tr[i].find_all('td')

        time = time.replace(hour=j)
        event = Archive(date=time, character=td[3].text,
                        temp_a=td[5].text, temp_b=td[5].text,
                        wind_speed_a=td[1].text, wind_speed_b=td[1].text)
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

        time = datetime.now() + timedelta(days=1)
        time = time.replace(hour=k)
        event = Rp5(date=time, character=character_out,
                    temp_a=temp_a_out, temp_b=temp_b_out,
                    wind_speed_a=wind_out, wind_speed_b=wind_out)
        db.session.add(event)
        db.session.commit()


def gismeteo():
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

    for i, j, k, h, r in zip(weather_out, temp_out, speed_a_out, speed_b_out, [5, 11, 17, 23]):
        time = datetime.now() + timedelta(days=1)
        time = time.replace(hour=r)

        event = Gismeteo(date=time, character=i,
                         temp_a=j, temp_b=j,
                         wind_speed_a=k, wind_speed_b=h)
        db.session.add(event)
        db.session.commit()


def yandex():
    # утро - 5:00  'morning' день - 11 'day' вечер 17 'evening' ночь 23 'night'
    # характер погоды : осадки и облачки 'condition' 'cloudness'
    # температура + - 0 'temp_avg'
    # ветер м/c 'wind_speed'
    url = 'https://api.weather.yandex.ru/v2/forecast?lat=58.010454&lon=56.229441&lang=ru_RU&limit=2&hours=true&extra=true'
    response = requests.get(url, headers={'X-Yandex-API-Key': 'adae34d0-0276-4494-987d-4051576fcd3c'}).json()
    count = 1
    for part in response['forecasts']:
        if count == 1:
            count = 2
        else:
            day_condition = part['parts']['day']['condition']
            day_cloudness = part['parts']['day']['cloudness']
            day_temp = part['parts']['day']['temp_avg']
            day_wind = part['parts']['day']['wind_speed']
            #
            night_condition = part['parts']['night']['condition']
            night_cloudness = part['parts']['night']['cloudness']
            night_temp = part['parts']['night']['temp_avg']
            night_wind = part['parts']['night']['wind_speed']
            #
            morning_condition = part['parts']['morning']['condition']
            morning_cloudness = part['parts']['morning']['cloudness']
            morning_temp = part['parts']['morning']['temp_avg']
            morning_wind = part['parts']['morning']['wind_speed']
            #
            evening_condition = part['parts']['evening']['condition']
            evening_cloudness = part['parts']['evening']['cloudness']
            evening_temp = part['parts']['evening']['temp_avg']
            evening_wind = part['parts']['evening']['wind_speed']

            mas_weather = [[morning_condition, morning_cloudness, morning_temp, morning_wind],
                           [day_condition, day_cloudness, day_temp, day_wind],
                           [evening_condition, evening_cloudness, evening_temp, evening_wind],
                           [night_condition, night_cloudness, night_temp, night_wind]]
            for row, j in zip(mas_weather, [5, 11, 17, 23]):
                time = datetime.now() + timedelta(days=1)
                time = time.replace(hour=j)
                cloudness = ""
                if row[1] == 0:
                    cloudness = "Ясно"
                if row[1] == 0.25:
                    cloudness = "Малооблачно"
                if row[1] == 0.5:
                    cloudness = "Облачно с прояснениями"
                if row[1] == 0.75:
                    cloudness = "Облачно с прояснениями"
                if row[1] == 1:
                    cloudness = "Пасмурно"

                event = Yandex(date=time, character=str(row[0] + " " + cloudness),
                               temp_a=row[2], temp_b=row[2],
                               wind_speed_a=row[3], wind_speed_b=row[3])
                db.session.add(event)
                db.session.commit()


if __name__ == '__main__':
    app.run()
