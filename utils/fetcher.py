import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import re


def get_articles(sources):
    '''
    (1) Iterates through all sources
    (2) Performs html request
    (3) Parses response
    (4) Writes headlines to csv
    '''

    # open csv file in write mode, with two columns {'Source', 'Title'}
    outfile = open("./headlines.csv", "w")
    writer = csv.writer(outfile)
    writer.writerows([['Source', 'Title']])

    session = requests.session()

    # iterate through each source and perform an html request, parse data using beautiful soup, and process text
    for s in sources:

        response = session.get(s['url'], headers={'Accept-Encoding': 'identity, deflate, compress, gzip', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
        html = response.content
        soup = BeautifulSoup(html, "html.parser")

        story_headings = soup.findAll(s['elem'], attrs={'class': s['class']})

        rows = []
        for headline in story_headings:
            headline = re.sub(r'[^\w\s]', '', headline.text)
            rows.append([s['source'], headline.strip()])

        writer.writerows(rows)
