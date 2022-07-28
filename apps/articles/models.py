from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
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


class LessInterestArticles(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, related_name='less_interest_article', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='less_interest_article', on_delete=models.CASCADE)
