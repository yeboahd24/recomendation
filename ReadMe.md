# user-customized area for general recommendations

# usage

```bash
docker compose up
docker exec -it longevity_web_1 bash

python manage.py migrate
# crawl all articles since many articles do not have title and abstract
# python manage.py runscript get_articles
python manage.py runscript populate

# test recommendation
# More pregnancy related articles as input, less related articles are recommended
python manage.py test
# output: 
#pregnancy article percentage:  20.77% (All articles)
#pregnancy article percentage:  20.93% input pregnancy articles:  0 iterations: 500 articles: 50
#pregnancy article percentage:  13.48% input pregnancy articles:  1 iterations: 500 articles: 50
#pregnancy article percentage:   6.34% input pregnancy articles:  3 iterations: 500 articles: 50
#pregnancy article percentage:   3.68% input pregnancy articles:  6 iterations: 500 articles: 50
#pregnancy article percentage:   3.28% input pregnancy articles: 15 iterations: 500 articles: 50


# test recommendation with a specific user

export DJANGO_SUPERUSER_PASSWORD=admin;python manage.py createsuperuser --username admin --email admin@admin.com --no-input --skip-checks 
python manage.py runserver

# go to http://localhost:8000/articles/?count-word=xxx to interactively test the recommendation
# After close some articles, refresh the page to see the new recommendations.

# ex: http://localhost:8000/articles/?count-word=pregnanc&total=50
# After few pregnancy related articles are closed, pregnancy related articles will show up less frequently.
```