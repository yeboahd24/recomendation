import requests
from pyquery import PyQuery as pq
import re
import pandas as pd
from pathlib import Path
import csv
from tqdm import tqdm


def get_article(url, index):
    content = requests.get(url)
    # print(content.content)
    d = pq(content.content.decode())
    title = d('.heading-title').eq(0).text() or 'NO_TITLE'
    try:
        abstract = d('.abstract-content').eq(0).text() or 'NO_ABSTRACT'
    except:
        abstract = 'NO_ABSTRACT'
    try:
        affiliations = d('.affiliations').eq(0).text() or 'NO_AFFILIATIONS'
    except:
        affiliations = 'NO_AFFILIATIONS'
    authors = re.sub(r'(\xa0(\s+\d+)*\s*)', ' ', d('.authors-list').eq(0).text())
    journal = d('.journal-actions-trigger').eq(0).text()
    date = d('.cit').eq(0).text().split(';')[0]
    keywords = ','.join(_.text() for _ in d('.keyword-actions-trigger').items())
    return [index, title, abstract, affiliations, authors, journal, date, keywords, url]


def run():
    keys = """,title,abstract,affiliations,authors,journal,date,keywords,url"""
    path = Path(__file__).resolve().parent.joinpath('articles.org.csv')
    articles = pd.read_csv(f'{Path(__file__).resolve().parent}/articles.org.csv')
    articles['abstract'] = articles['abstract'].replace('NO_ABSTRACT', "")
    articles['title'] = articles['abstract'].replace('NO_TITLE', "")
    article_path = path.with_name('article.csv')
    if article_path.exists():
        if not str(input(f'Override {article_path.name}? (Yes/No)')).lower().strip().startswith('yes'):
            return
    with article_path.open('w') as file:
        bar = tqdm(total=len(articles.index))
        writer = csv.writer(file)
        writer.writerow(keys.split(','))
        for index, row in articles.iterrows():
            bar.desc = f'{index=}'
            bar.update()
            writer.writerow([str(_).replace('\n', ' ') for _ in get_article(row.url, index)])


if __name__ == '__main__':
    run()
