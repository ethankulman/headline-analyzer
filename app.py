import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from utils.fetcher import checker
from utils.parser import parser
from utils.language_processor import analyzer
from utils.charts import daily_split, trump_tracker
import jinja2
import datetime

# must export FLASK_APP, DATABASE_URL,
# export FLASK_APP=app.py
# export DATABASE_URL=""
# export google credentials


sources = [{'source': 'NyTimes', 'url': 'https://www.nytimes.com/section/politics', 'elem': 'h2', 'class': 'headline'},
          {'source': 'Breitbart', 'url': 'http://www.breitbart.com/big-government/', 'elem': 'h2', 'class': 'title'},
          {'source': 'Huffington', 'url': 'http://www.huffingtonpost.com/section/politics', 'elem': 'h2', 'class': 'card__headline'},
          {'source': 'Fox', 'url': 'http://www.foxnews.com/politics.html', 'elem': 'h2', 'class': 'title'}]

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


def add_today_data():
    check = checker(sources)
    if check:
        today = parser()
        daily = analyzer(today)
        daily_split(daily)
        trump_tracker()



class Word(db.Model):
    __tablename__ = "word"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(20))
    date = db.Column(db.DateTime(), default=datetime.date.today())
    source = db.Column(db.String())
    sentiment = db.Column(db.Float(), nullable=True)
    magnitude = db.Column(db.Float(), nullable=True)

    def __init__(self, word, source):
        self.word = word
        self.source = source

    def __repr__(self):
        return "<%s >" % self.word

class Headline(db.Model):
    __tablename__ = "headlines"
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(128))
    word_id = db.Column(db.Integer)

    def __init__(self, headline, word_id):
        self.headline = headline
        self.word_id = word_id

    def __repr__(self):
        return "<%s >" % self.headline


db.create_all()

@app.route('/')
def index():
    if request.method == "GET":
        #trump_tracker()
        return render_template('index.html')

@app.route("/update")
def updated():
    if request.method == "GET":
        add_today_data()
        return "Database Updated!"



@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True)
