# connect to the instagram Graph API

import requests


""" def getAccessToken():
    app_id = 'your_app_id'
    app_secret = 'your_app_secret'
    accesToken = requests.get(
        "https://graph.facebook.com/oauth/access_token?client_id={990551122349675}&client_secret={b3e29839e30c755f6c12e21ee79dd677}&grant_type=client_credentials").json()['access_token']
    print(accesToken) """


def upload_video_to_instagram():

    # Set the access token and Instagram user ID
    access_token = "EAAOE5qfHjmsBAKlZBQkje6ngKHdY11JLgxOE37PJanNZCGpPgUDYp9uaKosYcooUAWNJMUM0bVr56MY1ZABhWckDEI88A6jpVUPUcTXEIBw3XCjfZA6GlbqQ0NUH741QPZAzdQ7Kl6h6UFpKCiZArOzWoehUfBwzu2B7NjloHvzOthIOzZCj6xxFqk6ZAuLatZABAM4pvtwkgeFlC9Lwln5O9"
    user_id = "108710088789614"

    # Define the video file path and caption
    video_file = './video.mp4'
    caption = 'My awesome video'

    # Set the video file and caption as form data
    data = {'video': open(video_file, 'rb'), 'caption': caption}

    # Define the headers for the API request
    headers = {
        'Content-Type': 'application/octet-stream',
        'Accept': 'application/json'
    }

    # Make the API request to upload the video
    response = requests.get(
        f"https://graph.facebook.com/{user_id}/accounts?access_token={access_token}")
    print(response.json())
