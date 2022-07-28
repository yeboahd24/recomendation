import random
import time
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Iterable
from pathlib import Path
from apps.articles.models import Article
import csv

articles = Article.objects.all()
articles_file = Path(__file__).resolve().parent.joinpath('articles.csv')
with articles_file.open('w') as fout:
    keys = """id,created_at,updated_at,title,abstract,body,affiliations,journal,authors,keywords,url""".split(',')
    writer = csv.writer(fout)
    writer.writerow(keys)
    for row in articles:
        writer.writerow([getattr(row, key) for key in keys])

articles = pd.read_csv(articles_file)
articles['abstract'] = articles['abstract'].replace('NO_ABSTRACT', '')
articles['info'] = articles['title'] + " " + articles['abstract']
articles['info'] = articles['info'].fillna('')
# print(articles.shape)
id_to_index = {
    row.id: index for index, row in articles.iterrows()
}
# print(id_to_index)

vectorizer = TfidfVectorizer(stop_words='english')
matrix = vectorizer.fit_transform(articles['info'])
similarity_matrix = cosine_similarity(matrix, matrix)

last_max = None


def get_articles_recommendations_ids(less_interest_ids: Iterable[int], k=20) -> list[int]:
    """
    get articles recommendations from less interests articles with cosine similarity

    performance for 1010 articles: less than 1 ms on 2019 i9 Macbook pro

    Not suitable for large dataset

    :param less_interest_ids: article indices of less interests articles
    :param k: number of articles to recommend
    :return: list of indices of articles recommendations
    """
    size = similarity_matrix.shape[0]
    if less_interest_ids:
        avg = None
        count = 0
        for article_id in less_interest_ids:

            # database id to matrix index
            index = id_to_index.get(article_id, -1)

            # ignore out of range index
            if index >= size or index < 0:
                continue

            count += 1
            if avg is None:
                avg = similarity_matrix[index].copy()
                continue
            avg += similarity_matrix[index]

        if avg is not None and count > 0:
            avg = avg / count
            max_val = np.max(avg)

            if max_val is np.nan or max_val <= 0:
                max_val = 1

            avg = (1 - avg / max_val)

            # make it more sensitive for less interest articles
            avg[avg < 0.88] *= 0.1
            avg[avg < 0.95] *= 0.75

            scores = dict(enumerate(avg))
            weights = [scores[_] for _ in range(size)]
        else:
            weights = None
    else:
        weights = None
    try:
        recommendations = random.choices(range(size), weights=weights, k=k)
    except Exception as e:
        print(e)
        raise
    return [articles.iloc[_].id for _ in recommendations]


def get_articles_recommendations(less_interest_articles: list[Article], k=20):
    ids = get_articles_recommendations_ids(less_interest_ids=[_.article_id for _ in less_interest_articles], k=k)
    return Article.objects.filter(id__in=ids).all()


if __name__ == "__main__":
    start = time.time()
    get_articles_recommendations_ids([0, 4, 3, 627, 838, 47, 534])
    print(time.time() - start)
