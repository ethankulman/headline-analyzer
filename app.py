import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from utils.fetcher import checker
from utils.parser import parser
from utils.language_processor import analyzer
from utils.charts import daily_split
from utils.celery_setup import make_celery
from datetime import datetime, timedelta
import jinja2

sources = [{'source': 'NyTimes', 'url': 'https://www.nytimes.com/section/politics', 'elem': 'h2', 'class': 'headline'},
          {'source': 'Breitbart', 'url': 'http://www.breitbart.com/big-government/', 'elem': 'h2', 'class': 'title'},
          {'source': 'Huffington', 'url': 'http://www.huffingtonpost.com/section/politics', 'elem': 'h2', 'class': 'card__headline'},
          {'source': 'Fox', 'url': 'http://www.foxnews.com/politics.html', 'elem': 'h2', 'class': 'title'}]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

db = SQLAlchemy(app)

celery = make_celery(app)


@celery.task(name="tasks.data")
def add_today_data():
    check = checker(sources)
    if check:
        today = parser()
        daily = analyzer(today)
        daily_split(daily)


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(20))
    date = db.Column(db.Date())
    source = db.Column(db.String())
    headlines = db.Column(db.ARRAY(str))
    sentiment = db.Column(db.Float())
    magnitude = db.Column(db.Float())

    def __init__(self, word, source, headlines, sentiment, magnitude):
        self.word = word
        self.source = source
        self.headlines = headlines
        self.sentiment = sentiment
        self.magnitude = magnitude


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    tomorrow = datetime.utcnow() + timedelta(days=1)
    result = add_today_data.apply_async(eta=tomorrow)
    app.run(debug=True)
