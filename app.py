from flask import Flask, render_template
from gismeteo import get_gis

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    get_gis()
    app.run()
