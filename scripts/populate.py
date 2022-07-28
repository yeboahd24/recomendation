import pandas as pd
from apps.articles.models import Article, LessInterestArticles
from pathlib import Path


def run():
    print(f'{Path(__file__).resolve().parent}/articles.csv')
    articles = pd.read_csv(f'{Path(__file__).resolve().parent}/articles.csv')
    articles['abstract'] = articles['abstract'].replace('NO_ABSTRACT', "")
    articles['title'] = articles['title'].replace('NO_TITLE', "")
    articles['title'].fillna('')
    articles['abstract'].fillna('')
    Article.objects.all().delete()
    LessInterestArticles.objects.all().delete()
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(db_index=True, max_length=255)
    abstract = models.TextField()
    body = models.TextField()
    affiliations = models.TextField()
    journal = models.TextField()
    authors = models.CharField(max_length=255)
    keywords = models.CharField(db_index=True, max_length=255)
    url = models.CharField(max_length=255)
    """
    print(articles.iloc[0].title)
    # exit(0)
    for index, article in articles.iterrows():
        print(index, str(article.title)[:200].replace('\n', ' '))
        row = Article(
            title=str(article.title),
            abstract=str(article.abstract),
            body='',
            affiliations=article.affiliations,
            journal=article.journal,
            authors=article.authors,
            keywords=article.keywords,
            url=article.url,
            id=index + index
        )
        row.save()
