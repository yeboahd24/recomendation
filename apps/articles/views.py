from django.views import *
from django.shortcuts import render
from apps.articles.models import Article, LessInterestArticles
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse


class ArticleRecommendationsView(View):
    @method_decorator(login_required(login_url='/admin/'))
    def get(self, request):
        from apps.recommenders.recommender import get_articles_recommendations
        total = int(request.GET.get('total', 20))
        user = request.user
        less_interested_articles = []
        if user:
            less_interested_articles = LessInterestArticles.objects.filter(user=user).all()
        articles = get_articles_recommendations(less_interested_articles, k=total)
        count_word = request.GET.get('count-word')
        count = 0
        if count_word:
            count = sum(count_word in article.title + article.abstract for article in articles)
        return render(request, 'articles/articles.html', dict(articles=articles, count_word=count_word, count=count))


@login_required(login_url='/admin/')
def close_article(request):
    args = request.GET.get('article_id')
    article = Article.objects.get(pk=args)
    if article is not None:
        if not LessInterestArticles.objects.filter(article=article, user=request.user).exists():
            LessInterestArticles(article=article, user=request.user).save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error', 'msg': 'Article not found'})
