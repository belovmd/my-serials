import tmdbsimple as tmdb


tmdb.API_KEY = '71af347ad6265c67d36f595aa27ea28c'


# response = tmdb.Search().tv(query='The Flash')
# print(response['results'])

# response = tmdb.TV_Seasons(60735, 6)
# print(response)

tv = tmdb.TV(60735)
response = tv.info()
print(response['next_episode_to_air'])
