import requests

api_token = '1011249006:AAEEWYV0BqIrRkHkLMt2rT-wztmr5nXRHa0'

requests.get('https://api.telegram.org/bot{}/sendMessage'.format(api_token),
             params=dict(
                 chat_id='@my_channel_name',
                 text='Hello world!'
             ))
