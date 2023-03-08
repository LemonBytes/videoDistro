

import requests


def upload_video_to_tiktok():

    CLIENT_KEY = 'awh4hp8rud5eu512'
    CLIENT_SECRET = 'e55484cc54f9b6863ec4b5974543ca74'
    code = requests.get('https://open-api.tiktok.com/oauth/')

    url_access_token = 'https://open-api.tiktok.com/oauth/access_token/'
    url_access_token + '?client_key=' + CLIENT_KEY
    url_access_token + '&client_secret=' + CLIENT_SECRET
    url_access_token + '&code=' + "wyzbits.com"
    url_access_token + '&grant_type=authorization_code'
    r = requests.post('https://open-api.tiktok.com/oauth/access_token/')
    print(r.text)
