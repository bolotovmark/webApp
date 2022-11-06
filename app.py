from flask import Flask, render_template
from scraper import get_bs
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    get_bs()
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
