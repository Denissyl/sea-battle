import os

from flask import Flask, render_template

from data.db_session import global_init

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    global_init('db/seabattle.sqlite')
    port = int(os.environ.get('PORT', 7000))
    app.run('0.0.0.0', port)
