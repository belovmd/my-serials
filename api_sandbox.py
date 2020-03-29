import tmdbsimple as tmdb

tmdb.API_KEY = '71af347ad6265c67d36f595aa27ea28c'

search_result = tmdb.Search().tv()['results']
print(search_result)

# python manage.py test --with-coverage
# python manage.py test --cover-package my_serials
