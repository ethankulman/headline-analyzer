import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import re

sources = [{'source': 'NyTimes', 'url': 'https://www.nytimes.com/section/politics', 'elem': 'h2', 'class': 'headline'},
          {'source': 'Breitbart', 'url': 'http://www.breitbart.com/big-government/', 'elem': 'h2', 'class': 'title'},
          {'source': 'Huffington', 'url': 'http://www.huffingtonpost.com/section/politics', 'elem': 'h2', 'class': 'card__headline'},
          {'source': 'Fox', 'url': 'http://www.foxnews.com/politics.html', 'elem': 'h2', 'class': 'title'}]

def get_articles(sources):
    outfile = open("./headlines.csv", "wb")
    writer = csv.writer(outfile)
    writer.writerows([['Source', 'Title']])
    session = requests.session()
    for s in sources:
        response = session.get(s['url'], headers={'Accept-Encoding': 'identity, deflate, compress, gzip', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        story_headings = soup.findAll(s['elem'], attrs={'class': s['class']})
        rows = []
        for r in story_headings:
            r = re.sub(r'[^\w\s]', '', r.text.encode("utf-8"))
            rows.append([s['source'], r.strip()])
        writer.writerows(rows)


def checker(sources):
    finished = True
    try:
        get_articles(sources)
        rt = pd.read_csv('./headlines.csv')
        for s in sources:
            n = rt['Source'] == s['source']
            try:
                n = rt[n]
                if len(n) > 1:
                    continue
                else:
                    finished = False
                    break
            except KeyError:
                finished = False
                break
    except urlfetch.Error:
        finished = False
    if not finished:
        checker(sources)
    return True


checker(sources)
