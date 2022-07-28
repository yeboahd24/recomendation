from unittest import TestCase
from apps.recommenders.recommender import *


class TestRecommenders(TestCase):

    @staticmethod
    def count_articles(indices: list[int], word='pregnanc'):
        # print(indices)
        return sum(
            word in str(articles.iloc[id_to_index.get(_)].title) + str(articles.iloc[id_to_index.get(_)].abstract) for _
            in indices)

    @classmethod
    def get_articles_and_count_avg(cls, indices: list[int], rounds=500, k=50):
        avg = 0
        assert rounds > 0
        for _ in range(rounds):
            avg += cls.count_articles(get_articles_recommendations_ids(indices[:], k=k))
        return avg / rounds

    def test_recommenders(self):
        keyword = 'pregnanc'
        rounds = 500
        pregnancy_articles = Article.objects.filter(title__contains=keyword)
        pregnancy_indices = []
        for _ in pregnancy_articles[:15]:
            pregnancy_indices.append(_.id)

        k = 50
        counter = 0
        for index in range(len(articles.index)):
            row = articles.iloc[index]
            if keyword in (str(row.title) + str(row.abstract)):
                counter += 1
        pregnancy_article_count_avg = counter / len(articles.index)
        print(f'pregnancy article percentage: {pregnancy_article_count_avg * 100:>6.2f}% (All articles)')
        result = []
        for num in [0, 1, 3, 6, len(pregnancy_indices)]:
            random.shuffle(pregnancy_indices)
            pregnancy_article_count_avg = self.get_articles_and_count_avg(pregnancy_indices[:num], rounds=rounds) / k
            print(
                f'pregnancy article percentage: {pregnancy_article_count_avg * 100:>6.2f}% '
                f'input pregnancy articles: {num:>2} '
                f'iterations: {rounds:>3} articles: {k:>2}')
            result.append(pregnancy_article_count_avg)
        self.assertEqual(result, sorted(result, reverse=True))
