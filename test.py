import tmdbsimple as tmdb


tmdb.API_KEY = '71af347ad6265c67d36f595aa27ea28c'


# response = tmdb.Search().tv(query='The Flash')
# print(response['results'])

# response = tmdb.TV_Seasons(60735, 6)
# print(response)
#
# tv = tmdb.TV(60735)
# response = tv.info()
# print(response)
# print(response['next_episode_to_air'])

search_result = tmdb.Search().tv(query='the flash')
print(search_result)
# lst = {s['id']: tmdb.TV(s['id']).info()['in_production'] for s in search_result['results']}
# print(lst)

# tv = tmdb.TV(44217).info()
# print(tv)
# result = {
#     'next_date': tv['next_episode_to_air']['air_date'],
#     'next_name': tv['next_episode_to_air']['name'],
#     'overview': tv['next_episode_to_air']['overview'],
# }


