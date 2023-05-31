import uuid
from pytube import YouTube


url = "https://www.youtube.com/watch?v=mOV6p5kPDgA"




def __download_from_youtube(counter=0):
        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            stream.download("./last_video_download/", "video.mp4")  # type: ignore
            print("finished downloading video")
        except Exception as e:
            if counter > 10:
                print(e)
                raise Exception("Error downloading video")
            __download_from_youtube(counter=counter + 1)


        


def __extract_video_id(url):
        video_id = str(uuid.uuid5(uuid.NAMESPACE_URL, url))
        print(video_id)

__extract_video_id(url)