from pytube import YouTube


url = "https://youtube.com/watch?v=dPJCtzWeToE&feature=share"




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


__download_from_youtube()            