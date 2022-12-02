import os
from flask import Flask, render_template
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

from parse.archive_parse import get_archive
from parse.gismeteo import get_gis
from parse.yandex_api import parse_weather
from parse.rp5 import get_bs

app = Flask(__name__)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@scheduler.task('interval', id='do_job_1', seconds=5)
def scheduled_task():
    #get_archive()
    pass


if __name__ == '__main__':

    app.run()
