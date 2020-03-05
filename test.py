import tmdbsimple as tmdb


tmdb.API_KEY = '71af347ad6265c67d36f595aa27ea28c'


search = tmdb.Search()
response = search.tv(query='The Flash')
for s in search.results:
    print(s['poster_path'])

