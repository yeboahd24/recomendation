from django.db import migrations
from django.db import models
from apps.articles.models import *
from django.conf import settings


# from django.contrib.auth import get_user_model

class Migration(migrations.Migration):
    dependencies = [
        ('articles', '0001_initial')
    ]
    initial = True
    operations = [
        migrations.CreateModel(
            name='LessInterestArticles',
            fields=[
                # ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=models.deletion.CASCADE,
                                              related_name='less_interest_article',
                                              to="articles.Article")),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE,
                                           related_name='less_interest_article',
                                           to='auth.User')),
            ]
        )
    ]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['article', 'user'], name='unique_less_interest_article'
            )
        ]
