import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload


def upload_video_to_youtube():

    text_file = open("texts/titles.txt", "r")
    # take the last line of the file
    title = text_file.readlines()[-1]
    text_file.close()
    if title != "":
        scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secrets.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = youtube.videos().insert(
            part="snippet",
            body={
                "kind": "youtube#shorts",
                "snippet": {
                    "title": f'{title}',
                    "description": "A fight is a physical manifestation of the interplay between the body and mind. The body is the vehicle through which the mind expresses itself, and the mind is the driver that directs the body's actions. In a fight, the body and mind work in tandem to overcome obstacles and achieve victory. The outcome of the fight depends on the harmony and synchronization between the body and mind, as well as the warrior's ability to stay present and centered amidst the chaos of battle."
                }
            },


            media_body=MediaFileUpload("../inputVideo/video.mp4")
        )
        response = request.execute()

        print(response)
