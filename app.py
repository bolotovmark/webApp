from flask import Flask, render_template
from flask_apscheduler import APScheduler

from parse.archive_parse import get_archive
from parse.gismeteo import get_gis
from parse.yandex_api import parse_weather
from parse.rp5 import get_bs

app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@scheduler.task('interval', id='do_job_1', seconds=5)
def scheduled_task():
    get_archive()


if __name__ == '__main__':
    app.run()
