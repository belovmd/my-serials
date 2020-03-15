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

# search_result = tmdb.Search().tv(query='the flash')
# print(search_result)
# lst = {s['id']: tmdb.TV(s['id']).info()['in_production'] for s in search_result['results']}
# print(lst)

# tv = tmdb.TV(44217).info()
# print(tv)
# result = {
#     'next_date': tv['next_episode_to_air']['air_date'],
#     'next_name': tv['next_episode_to_air']['name'],
#     'overview': tv['next_episode_to_air']['overview'],
# }
# tv = tmdb.TV(60735)
# # tv_s = tmdb.TV_Seasons(60735, 1)
# seasons = tv.info()['seasons']
# tv_s = tmdb.TV_Seasons(60735, 1).info()
# print(tv_s)

# tv = tmdb.TV(82856)
# cast = tv.credits()
# print(cast)
tv = tmdb.TV_Seasons(60735, 1).
print(tv.info())
# print(seasons)
# for season in seasons:
#     tv_s = tmdb.TV_Seasons(60735, season['season_number']).info()['episodes']
#     season['episodes'] = tv_s
# print(seasons)
# print()

# print()
# print(tv_s.info()['episodes'])
# episodes_list = {}
# for season in tv.info()['seasons']:
#     tv_s = tmdb.TV_Seasons(60735, season['season_number']).info()['episodes']
#     print(tv_s)
    # episodes_list[season['season_number']] = tv_s
# print(episodes_list)
# print(tv.alternative_titles())
# print(tv.content_ratings())
# print(tv.credits())
# print(tv.images())
# # print(tv.rating())
# print(tv.similar())
# print(tv.recommendations())
# print(tv.translations())
# print(tv.videos())
# print(tv.latest())
# print(tv.on_the_air())
# print(tv.airing_today())
# print(tv.top_rated())
# print(tv.popular())
