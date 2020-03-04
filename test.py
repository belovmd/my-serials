import tmdbsimple as tmdb


tmdb.API_KEY = '71af347ad6265c67d36f595aa27ea28c'


serial_id = 1412
serial_db = tmdb.TV(serial_id)
response = serial_db.info()
title = response['name']
air_date = response['first_air_date'][0:4]
print(title)
print(air_date)
